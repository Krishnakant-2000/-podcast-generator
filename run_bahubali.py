import os
import sys

# Add ai_podcast_generator to path
PODCAST_DIR = r"C:\Users\USER\Desktop\ai_podcast_generator"
sys.path.insert(0, PODCAST_DIR)
os.chdir(PODCAST_DIR)

from bahubali_topic import BAHUBALI_TOPIC
import daily_cron
from upload_to_youtube import upload_video

def main():
    topic = BAHUBALI_TOPIC
    print(f"\n========================================================")
    print(f"  STARTING BAHUBALI EPISODE GENERATION: {topic['title']}")
    print(f"  Category: {topic['category']}")
    print(f"  Location: Shravanabelagola, Hassan District, Karnataka")
    print(f"========================================================\n")

    # 1. Build Videos: 1 Long-Form (subtitled, real images, 16:9) + 2 Shorts (9:16)
    long_mp4, short_a_mp4, short_b_mp4 = daily_cron.build_long_and_short_videos(topic)

    print(f"\n========================================================")
    print(f"  ALL VIDEOS RENDERED SUCCESSFULLY!")
    print(f"  Long-Form: {long_mp4}")
    print(f"  Short A:   {short_a_mp4}")
    print(f"  Short B:   {short_b_mp4}")
    print(f"========================================================\n")

    # 2. Upload Long-Form Video (16:9)
    print("🚀 Auto Uploading Deep Long-Form Subtitled Video (16:9)...")
    upload_video(
        video_path=long_mp4,
        title=f"{topic['title']} (Full Documentary)",
        description=f"{topic['long_scenes'][0]['text']} #AllAroundPodcast #{topic['category'].replace(' ', '')} #Bahubali #Shravanabelagola #Karnataka #AncientIndia #History",
        privacy="public"
    )

    # 3. Auto Upload Short Hook A (9:16)
    print("\n🚀 Auto Uploading YouTube Short Hook A (9:16)...")
    upload_video(
        video_path=short_a_mp4,
        title=topic.get("short_title_a", topic["title"]),
        description=f"{topic['short_scenes_a'][0]['text']} #Shorts #AllAroundPodcast #Bahubali #Karnataka",
        privacy="public"
    )

    # 4. Auto Upload Short Hook B (9:16)
    print("\n🚀 Auto Uploading YouTube Short Hook B (9:16)...")
    upload_video(
        video_path=short_b_mp4,
        title=topic.get("short_title_b", topic["title"]),
        description=f"{topic['short_scenes_b'][0]['text']} #Shorts #AllAroundPodcast #Gommateshwara #AncientMysteries",
        privacy="public"
    )

    # Update history.json
    history = daily_cron.load_history()
    if topic["id"] not in history:
        history.append(topic["id"])
        daily_cron.save_history(history)

    print(f"\n========================================================")
    print(f"🎉 BAHUBALI EPISODE SUCCESSFULLY GENERATED & UPLOADED!")
    print(f"========================================================\n")

if __name__ == "__main__":
    main()
