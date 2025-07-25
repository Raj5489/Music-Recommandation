from flask import Flask, render_template, request, jsonify
from emotion import detect_emotion_from_image
from youtube_api import get_music_by_emotion
import os
from werkzeug.utils import secure_filename
from PIL import Image
import traceback

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/start')
def index():
    return render_template('index.html')

@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/detect', methods=['POST'])
def detect():
    filepath = None  # define early for cleanup

    try:
        if 'image' not in request.files:
            print("[ERROR] No image part in request.")
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            print("[ERROR] Empty filename.")
            return jsonify({'error': 'Empty filename'}), 400

        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)

        print(f"[DEBUG] Saved file at: {filepath}")
        print(f"[DEBUG] File exists: {os.path.exists(filepath)}")
        print(f"[DEBUG] File size: {os.path.getsize(filepath)} bytes")

        # Load and verify image
        try:
            img = Image.open(filepath)
            img.verify()
            img = Image.open(filepath).convert('RGB')
            print("[DEBUG] Image loaded successfully.")
        except Exception as e:
            print("[ERROR] PIL failed to open image.")
            traceback.print_exc()
            return jsonify({'error': 'Invalid image format'}), 500

        # Emotion detection
        # Emotion detection
        try:
            result = detect_emotion_from_image(img)

            # If emotion.py returns both dominant emotion and scores
            if isinstance(result, tuple):
                emotion, emotion_scores = result
            else:
                emotion = result
                emotion_scores = None

            print(f"[DEBUG] Emotion detected: {emotion}")
            if emotion_scores:
                print("[DEBUG] Emotion Scores:")
                for emo, score in emotion_scores.items():
                    print(f"  {emo}: {score:.2f}")
        except Exception as e:
            print("[ERROR] Emotion detection failed.")
            traceback.print_exc()
            return jsonify({'error': 'Emotion detection failed'}), 500


        # Handle low-confidence or no-face results
        if emotion in ['no_face', 'uncertain', 'error']:
            print("[INFO] Emotion unclear or face not detected.")
            return jsonify({
                'error': 'Could not detect a clear emotion. Try a brighter image or more expressive face.'
            }), 200

        # Music recommendation
                # Music recommendation
        try:
            recommendations = get_music_by_emotion(emotion)
            print(f"[DEBUG] Fetched {len(recommendations)} recommendations.")
        except Exception as e:
            print("[ERROR] YouTube API failed.")
            traceback.print_exc()
            return jsonify({'error': 'Failed to get recommendations'}), 500
        
        print("[DEBUG] Emotion passed to YouTube:", emotion)
        print("[DEBUG] Music results:", recommendations)

        # ✅ This must be outside the except block
        return jsonify({
            'emotion': emotion,
            'emotion_scores': emotion_scores,
            'recommendations': recommendations
        })



    except Exception as e:
        print("[FATAL ERROR]", e)
        traceback.print_exc()
        return jsonify({'error': 'Unexpected server error'}), 500

    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            print(f"[DEBUG] Deleted file: {filepath}")

if __name__ == '__main__':
    app.run(debug=True)
