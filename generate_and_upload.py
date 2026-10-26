import os
import sys
import subprocess

"""
MASTER AUTO-GENERATOR & YOUTUBE UPLOADER

Generates both the 16:9 Full Episode Video AND the 9:16 YouTube Short,
and automatically uploads them to your YouTube Podcast Channel!

Usage:
  python generate_and_upload.py
"""

GENERATOR_SCRIPT = os.path.join(os.path.dirname(__file__), "generate_video.py")
UPLOADER_SCRIPT = os.path.join(os.path.dirname(__file__), "upload_to_youtube.py")

WIDESCREEN_MP4 = os.path.join(r"C:\Users\USER\Desktop", "Kailasa_Temple_Secrets_Episode1.mp4")
SHORTS_MP4 = os.path.join(r"C:\Users\USER\Desktop", "Kailasa_Temple_Secrets_Shorts.mp4")

if __name__ == "__main__":
    print("=========================================================")
    print("  STEP 1: GENERATING VIDEOS (16:9 Full & 9:16 Short)     ")
    print("=========================================================\n")

    # Run Video Generation
    subprocess.run([sys.executable, GENERATOR_SCRIPT], check=True)

    print("\n=========================================================")
    print("  STEP 2: AUTO-UPLOADING TO YOUTUBE                      ")
    print("=========================================================\n")

    # Upload Full Video (16:9)
    if os.path.exists(WIDESCREEN_MP4):
        print("Uploading Full Episode Video (16:9)...")
        subprocess.run([
            sys.executable, UPLOADER_SCRIPT,
            "--video", WIDESCREEN_MP4,
            "--title", "Unsolved Secrets of Kailasa Temple Ellora | Ancient Megalithic Mysteries #1",
            "--desc", "Discover how ancient sculptors carved 200,000 tons of rock top-to-bottom at Kailasa Temple, Ellora. #KailasaTemple #AncientMysteries #IndianHistory #Archeology",
            "--privacy", "public"
        ])

    # Upload YouTube Short (9:16)
    if os.path.exists(SHORTS_MP4):
        print("\nUploading YouTube Short Video (9:16)...")
        subprocess.run([
            sys.executable, UPLOADER_SCRIPT,
            "--video", SHORTS_MP4,
            "--title", "The Vanished Mountain of Kailasa Temple #Shorts #AncientMysteries",
            "--desc", "200,000 tons of rock vanished with zero debris found around Ellora. How was it built? #KailasaTemple #Shorts #IndianHistory #Archeology",
            "--privacy", "public"
        ])
