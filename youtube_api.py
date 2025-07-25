import requests

# 🔐 Insert your API key here
YOUTUBE_API_KEY = ""  # Replace with your actual API key

# 🧠 Emotion to music search query mapping
emotion_to_query = {
    'happy': 'happy songs',
    'sad': 'sad songs',
    'angry': 'rock metal music',
    'neutral': 'lofi chill music',
    'surprise': 'top pop hits',
    'fear': 'calming instrumental',
    'disgust': 'alternative rock'
}

def get_music_by_emotion(emotion, max_results=6):
    search_query = f"{emotion_to_query.get(emotion.lower(), 'chill music')} hindi english punjabi"
    print(f"[DEBUG] Emotion: {emotion}")
    print(f"[DEBUG] YouTube search query: {search_query}")

    # If no API key, return dummy list
    if not YOUTUBE_API_KEY.strip():
        print("[WARNING] No YouTube API key provided. Returning fallback music.")
        return [
            {"title": "Lofi Chill Beats to Relax/Study", "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"},
            {"title": "Coding Music Mix", "url": "https://www.youtube.com/watch?v=kcBztLVA9zk"},
            {"title": "Sad Piano Instrumental", "url": "https://www.youtube.com/watch?v=ijLJST0mDLs"}
        ]

    # Call YouTube API
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": search_query,
        "type": "video",
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])
        print(f"[DEBUG] YouTube returned {len(items)} items.")

        recommendations = [
            {
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            for item in items if "videoId" in item["id"]
        ]

        print(f"[DEBUG] Final Recommendations: {recommendations}")
        return recommendations or [{"title": "Default Music", "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"}]

    except Exception as e:
        print(f"[ERROR] YouTube API failed: {e}")
        return [{"title": "Default Music", "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"}]



# import requests

# YOUTUBE_API_KEY = "AIzaSyA1d_UPH8ssfTVvtvVFffTqftgg0ttE6_8"

# emotion_to_query = {
#     'happy': 'happy songs',
#     'sad': 'sad songs',
#     'angry': 'rock metal music',
#     'neutral': 'lofi chill music',
#     'surprise': 'top pop hits',
#     'fear': 'calming instrumental',
#     'disgust': 'alternative rock'
# }

# def get_music_by_emotion(emotion, max_results=6):
#     search_query = emotion_to_query.get(emotion.lower(), 'chill music')
#     url = "https://www.googleapis.com/youtube/v3/search"
#     params = {
#         "part": "snippet",
#         "q": search_query,
#         "type": "video",
#         "key": YOUTUBE_API_KEY,
#         "maxResults": max_results
#     }

#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         items = response.json().get("items", [])
#         recommendations = [
#             {
#                 "title": item["snippet"]["title"],
#                 "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
#             }
#             for item in items if "videoId" in item["id"]
#         ]
#         return recommendations
#     except Exception as e:
#         print(f"[ERROR] YouTube API failed: {e}")
#         return [{"title": "Default Track", "url": "https://www.youtube.com/watch?v=5qap5aO4i9A"}]
