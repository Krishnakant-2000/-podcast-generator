import os
import sys

PODCAST_DIR = r"C:\Users\USER\Desktop\ai_podcast_generator"
sys.path.insert(0, PODCAST_DIR)
os.chdir(PODCAST_DIR)

from upload_to_youtube import upload_video

def main():
    long_video = os.path.join(PODCAST_DIR, "uploads", "long_format", "Daily_Episode_13_Long_16_9.mp4")
    short_a = os.path.join(PODCAST_DIR, "uploads", "shorts", "Daily_Episode_13_ShortA_9_16.mp4")
    short_b = os.path.join(PODCAST_DIR, "uploads", "shorts", "Daily_Episode_13_ShortB_9_16.mp4")

    print("\n========================================================")
    print("  UPLOADING LEPAKSHI EPISODE 13 VIDEOS TO YOUTUBE")
    print("========================================================\n")

    # 1. Long Video
    print("🚀 1/3 Uploading Deep Long-Form Documentary (16:9)...")
    url_long = upload_video(
        video_path=long_video,
        title="The 500-Year-Old Pillar Defying Gravity: The Impossible Architecture of Lepakshi (Full Documentary)",
        description="Inside the 500-year-old Lepakshi Temple in Andhra Pradesh, one of its seventy massive stone pillars literally hangs in mid-air and does not touch the ground! Discover the mystery of the hanging pillar, the giant footprint of Sita, and the Vijayanagara architectural genius.\n\n#AllAroundPodcast #Lepakshi #HangingPillar #AndhraPradesh #AncientIndia #History #Mystery #Documentary",
        tags=["Lepakshi Temple", "Hanging Pillar", "Floating Pillar Lepakshi", "Ancient Indian Engineering", "All Around Podcast", "Andhra Pradesh History", "Vijayanagara Architecture", "Ancient Mysteries India"],
        privacy="public"
    )

    # 2. Short A
    print("\n🚀 2/3 Uploading YouTube Short Hook A (9:16)...")
    url_short_a = upload_video(
        video_path=short_a,
        title="The 500-Year-Old Hanging Pillar Defying Gravity at Lepakshi #Shorts",
        description="Inside the 500-year-old Lepakshi Temple in Andhra Pradesh, one of its seventy massive stone pillars literally hangs in mid-air!\n\n#Shorts #AllAroundPodcast #Lepakshi #FloatingPillar #AncientEngineering",
        tags=["Shorts", "Lepakshi Temple", "Hanging Pillar", "Ancient India", "All Around Podcast"],
        privacy="public"
    )

    # 3. Short B
    print("\n🚀 3/3 Uploading YouTube Short Hook B (9:16)...")
    url_short_b = upload_video(
        video_path=short_b,
        title="The Mystery of Lepakshi's Giant Footprint That Never Dries Up #Shorts",
        description="In the open stone courtyard of Lepakshi Temple lies a mysterious three-foot giant footprint pressed deeply into solid granite rock that never dries up!\n\n#Shorts #AllAroundPodcast #GiantFootprint #LepakshiMystery",
        tags=["Shorts", "Lepakshi Giant Footprint", "Ancient Mysteries", "Lepakshi", "All Around Podcast"],
        privacy="public"
    )

    print("\n========================================================")
    print("  🎉 ALL 3 VIDEOS SUCCESSFULLY UPLOADED TO YOUTUBE!")
    print(f"  Long-Form: {url_long}")
    print(f"  Short A:   {url_short_a}")
    print(f"  Short B:   {url_short_b}")
    print("========================================================\n")

if __name__ == "__main__":
    main()
