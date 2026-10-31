import os
import sys

PODCAST_DIR = r"C:\Users\USER\Desktop\ai_podcast_generator"
sys.path.insert(0, PODCAST_DIR)
os.chdir(PODCAST_DIR)

from iron_pillar_topic import IRON_PILLAR_TOPIC
import daily_cron

def main():
    topic = IRON_PILLAR_TOPIC
    print("\n========================================================")
    print(f"  STARTING EPISODE 14 GENERATION: {topic['title']}")
    print(f"  Category: {topic['category']}")
    print(f"  Location: Qutb Complex, Mehrauli, New Delhi, India")
    print("========================================================\n")

    # 1. Build Videos: 1 Long-Form (subtitled, real images, 16:9) + 2 Shorts (9:16)
    long_mp4, short_a_mp4, short_b_mp4 = daily_cron.build_long_and_short_videos(topic)

    print("\n========================================================")
    print("  🎉 ALL VIDEOS RENDERED SUCCESSFULLY WITH YOUR VOICE!")
    print(f"  Long-Form: {long_mp4}")
    print(f"  Short A:   {short_a_mp4}")
    print(f"  Short B:   {short_b_mp4}")
    print("========================================================\n")

    # Update history.json
    history = daily_cron.load_history()
    if topic["id"] not in history:
        history.append(topic["id"])
        daily_cron.save_history(history)

if __name__ == "__main__":
    main()
