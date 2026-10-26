import os
import sys
import asyncio
import requests
import edge_tts
from PIL import Image
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

"""
Universal AI Video Generator for Future Episodes
Run this script for any new topic!

Usage:
  python generate_custom_episode.py "Barabar Caves Ancient Laser Precision"
  python generate_custom_episode.py "Konark Sun Temple Floating Magnet Mystery"
  python generate_custom_episode.py "Panchatantra Sleep Story The Sacred Banyan Tree"
"""

VOICE = "en-IN-PrabhatNeural"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip().replace(' ', '_')

async def synthesize_audio(text, output_file):
    communicate = edge_tts.Communicate(text, VOICE, rate="-3%", pitch="-1Hz")
    await communicate.save(output_file)

def fetch_ai_image(prompt, output_file, seed):
    encoded = requests.utils.quote(f"{prompt}, 8k photorealistic, 16:9 widescreen, cinematic lighting")
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&nologo=true&seed={seed}"
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(res.content)
            return output_file
    except Exception as e:
        print(f"Image fetch error: {e}")

    img = Image.new("RGB", (1280, 720), color=(15, 10, 30))
    img.save(output_file)
    return output_file

def create_episode(topic_title, scene_data):
    clean_title = sanitize_filename(topic_title)
    final_mp4 = os.path.join(r"C:\Users\USER\Desktop", f"{clean_title}.mp4")

    print(f"\n==================================================")
    print(f"  CREATING EPISODE: {topic_title}")
    print(f"==================================================\n")

    clips = []
    for i, s in enumerate(scene_data):
        sid = i + 1
        a_path = os.path.join(OUTPUT_DIR, f"temp_a_{sid}.mp3")
        i_path = os.path.join(OUTPUT_DIR, f"temp_i_{sid}.jpg")

        print(f"🎙️ Generating Scene {sid} Audio & Image...")
        asyncio.run(synthesize_audio(s["text"], a_path))
        fetch_ai_image(s["prompt"], i_path, seed=200 + sid)

        audio_clip = AudioFileClip(a_path)
        img_clip = ImageClip(i_path).with_duration(audio_clip.duration + 0.5).with_audio(audio_clip)
        clips.append(img_clip)

    print("\n🎬 Rendering Final MP4 Video...")
    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(final_mp4, fps=24, codec="libx264", audio_codec="aac", preset="medium")

    print(f"\n🎉 SUCCESS! Generated: {final_mp4}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        title = sys.argv[1]
    else:
        title = "Barabar_Caves_Laser_Precision"

    # Default sample scene structure for Barabar Caves if invoked directly
    scenes = [
        {
            "text": f"Welcome back to Ancient Mysteries. Today we investigate {title}. One of the most perplexing structures in ancient history.",
            "prompt": f"Ancient Indian megalithic architecture {title}, dramatic fog, cinematic lighting, 8k"
        },
        {
            "text": "Carved inside solid granite cliffs, these chambers exhibit near-perfect geometric symmetry and mirror-like wall polish that remains smooth 2300 years later.",
            "prompt": "Mirror polished ancient granite cave interior India, reflection, volumetric lighting, photorealistic 8k"
        },
        {
            "text": "How did ancient builders polish rock as hard as granite to a mirror sheen without modern power tools or diamond abrasives?",
            "prompt": "Ancient Indian masons working on granite caves with glowing energy, ancient history, mysterious cinematic 8k"
        },
        {
            "text": "Subscribe for more unsolved ancient engineering marvels and tell us your thoughts in the comments below.",
            "prompt": "Epic aerial sunset view of ancient Indian granite mountain caves, golden light, 8k resolution"
        }
    ]

    create_episode(title, scenes)
