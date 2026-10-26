import os
import sys
from upload_to_youtube import get_authenticated_service

# Live video ID mapping with high-CTR, curiosity-driven titles
VIDEOS_TO_UPDATE = [
    {
        "id": "tCOK3hoa2KA",
        "title": "Did 200,000 Tons of Rock Really Just Vanish? The Kailasa Temple Paradox",
        "tags": ["KailasaTemple", "ElloraCaves", "AncientEngineering", "IndianHistory", "Archaeology"]
    },
    {
        "id": "s2u1RfMM8lE",
        "title": "How Did They Carve a Mountain TOP-TO-BOTTOM 1,200 Years Ago? #Shorts",
        "tags": ["Shorts", "KailasaTemple", "AncientHistory", "Megalithic"]
    },
    {
        "id": "2n1OOefdxnQ",
        "title": "Why This 2,300-Year-Old Granite Cave Echoes for 30 Seconds",
        "tags": ["BarabarCaves", "AncientIndia", "Megalithic", "AcousticMystery"]
    },
    {
        "id": "2H06dv06Ye4",
        "title": "Did Ancient Indians Have 3D Laser-Cutters 2,300 Years Ago? #Shorts",
        "tags": ["Shorts", "BarabarCaves", "AncientEngineering", "Megalithic"]
    },
    {
        "id": "BD1mXTAdHQ0",
        "title": "Fall Asleep in 5 Minutes: The Sacred Banyan Tree Bedtime Story",
        "tags": ["SleepStory", "BedtimeStory", "Panchatantra", "Relaxation", "DeepSleep"]
    },
    {
        "id": "QUNpB6WO-Vo",
        "title": "Listen to This Before You Go to Sleep Tonight 🌙 #Shorts",
        "tags": ["Shorts", "SleepStory", "BedtimeStory", "Relaxing"]
    },
    {
        "id": "KVlRcJ25Tcg",
        "title": "The 52-Ton Floating Magnet That Ruined Portuguese Ships",
        "tags": ["KonarkSunTemple", "AncientEngineering", "IndianHistory", "FloatingMagnet"]
    },
    {
        "id": "2llq4zQ_nFA",
        "title": "Why Portuguese Sailors Destroyed This 52-Ton Floating Magnet #Shorts",
        "tags": ["Shorts", "KonarkSunTemple", "AncientHistory", "FloatingMagnet"]
    },
    {
        "id": "Gy5HGl3fCkg",
        "title": "Deep Sleep Bedtime Story: Midnight Legends of Ancient Ujjain",
        "tags": ["SleepStory", "BedtimeStory", "VikramBetal", "Ujjain", "DeepSleep"]
    },
    {
        "id": "-hJMcZaHKw0",
        "title": "Instant Relaxation for Deep Sleep Tonight 🌌 #Shorts",
        "tags": ["Shorts", "SleepStory", "BedtimeStory", "Relaxation"]
    }
]

def update_video_metadata():
    print("🔑 Authenticating with YouTube Data API...")
    youtube = get_authenticated_service()

    for item in VIDEOS_TO_UPDATE:
        vid_id = item["id"]
        new_title = item["title"]
        tags = item["tags"]

        try:
            res = youtube.videos().list(part="snippet", id=vid_id).execute()
            if not res.get("items"):
                print(f"⚠️ Video [{vid_id}] not found on YouTube channel.")
                continue

            snippet = res["items"][0]["snippet"]
            snippet["title"] = new_title
            snippet["tags"] = tags

            youtube.videos().update(
                part="snippet",
                body={
                    "id": vid_id,
                    "snippet": snippet
                }
            ).execute()
            print(f"✅ Updated Title for [{vid_id}]: '{new_title}'")
        except Exception as e:
            print(f"❌ Failed to update [{vid_id}]: {e}")

if __name__ == "__main__":
    update_video_metadata()
