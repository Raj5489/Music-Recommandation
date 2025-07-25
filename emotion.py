from fer import FER
import numpy as np
import cv2
import traceback

# Confidence threshold (optional, tune this)
CONFIDENCE_THRESHOLD = 0.5

def detect_emotion_from_image(pil_image):
    try:
        print("[DEBUG] Starting FER-based emotion detection...")

        # Convert PIL image to OpenCV (BGR format)
        img = cv2.cvtColor(np.array(pil_image.convert('RGB')), cv2.COLOR_RGB2BGR)

        # Initialize FER detector
        detector = FER(mtcnn=True)

        # Detect emotions
        results = detector.detect_emotions(img)

        if not results:
            print("[ERROR] No face detected.")
            return "no_face"

        emotions = results[0]["emotions"]

        # Sort emotions by confidence
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        top_emotion, top_score = sorted_emotions[0]
        second_emotion, second_score = sorted_emotions[1]

        # Boost sad if it’s close to the top
        if second_emotion == "sad" and (top_score - second_score) < 0.05:
            print("[DEBUG] 'Sad' emotion very close to top. Overriding.")
            dominant_emotion = "sad"
            confidence = second_score
        else:
            dominant_emotion = top_emotion
            confidence = top_score


        print("[DEBUG] All emotion scores:")
        for emo, score in emotions.items():
            print(f"  {emo}: {score*100:.2f}%")
            if emotions.get("sad", 0) > 0.3:
                print("[INFO] Sad detected, just not dominant.")


        print(f"[DEBUG] Dominant Emotion: {dominant_emotion} ({confidence*100:.2f}%)")

        if confidence < CONFIDENCE_THRESHOLD:
            print("[WARNING] Low confidence emotion detected.")
            return "uncertain"

        return dominant_emotion, emotions

    except Exception as e:
        print("[ERROR] FER emotion detection failed:")
        traceback.print_exc()
        return "error"
