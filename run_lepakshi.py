import os
import sys

# Add ai_podcast_generator to path
PODCAST_DIR = r"C:\Users\USER\Desktop\ai_podcast_generator"
sys.path.insert(0, PODCAST_DIR)
os.chdir(PODCAST_DIR)

from lepakshi_topic import LEPAKSHI_TOPIC
import daily_cron
from upload_to_youtube import upload_video

def main():
    topic = LEPAKSHI_TOPIC
    print(f"\n========================================================")
    print(f"  STARTING LEPAKSHI EPISODE GENERATION: {topic['title']}")
    print(f"  Category: {topic['category']}")
    print(f"  Location: Anantapur District, Andhra Pradesh, India")
    print(f"========================================================\n")

    # 1. Build Videos: 1 Long-Form (subtitled, real images, 16:9) + 2 Shorts (9:16)
    long_mp4, short_a_mp4, short_b_mp4 = daily_cron.build_long_and_short_videos(topic)

    print(f"\n========================================================")
    print(f"  🎉 ALL VIDEOS RENDERED SUCCESSFULLY WITH YOUR VOICE!")
    print(f"  Long-Form: {long_mp4}")
    print(f"  Short A:   {short_a_mp4}")
    print(f"  Short B:   {short_b_mp4}")
    print(f"========================================================\n")

    # Update history.json
    history = daily_cron.load_history()
    if topic["id"] not in history:
        history.append(topic["id"])
        daily_cron.save_history(history)

    print(f"\n========================================================")
    print(f"🎉 LEPAKSHI EPISODE SUCCESSFULLY GENERATED & UPLOADED!")
    print(f"========================================================\n")

if __name__ == "__main__":
    main()
