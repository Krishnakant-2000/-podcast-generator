import os
import io
import sys
import textwrap
import asyncio
import requests
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# =============================================================================
# CONFIGURATION & OUTPUT PATHS
# =============================================================================
VOICE = "en-IN-PrabhatNeural"  # Deep, cinematic Indian male neural voice
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

WIDESCREEN_MP4 = os.path.join(r"C:\Users\USER\Desktop", "Kailasa_Temple_Secrets_Episode1.mp4")
SHORTS_MP4 = os.path.join(r"C:\Users\USER\Desktop", "Kailasa_Temple_Secrets_Shorts.mp4")

# =============================================================================
# SCRIPT & SCENE DEFINITION (Episode 1: Kailasa Temple Ellora)
# =============================================================================
SCENES = [
    {
        "id": 1,
        "narrative": (
            "Welcome to Ancient Mysteries Unveiled. Deep in Maharashtra, India, "
            "lies a structure that challenges everything we know about ancient engineering—"
            "The Kailasa Temple at Ellora."
        ),
        "search_term": "Ellora Caves India Kailasa Temple"
    },
    {
        "id": 2,
        "narrative": (
            "Unlike traditional buildings constructed from brick or stone blocks, "
            "Kailasa was carved top-to-bottom. Ancient sculptors removed over 200,000 tons "
            "of solid basalt rock using only hammers and chisels."
        ),
        "search_term": "Kailasa Temple Ellora courtyard reliefs"
    },
    {
        "id": 3,
        "narrative": (
            "Historians estimate it took 18 years of continuous labor to carve this monument. "
            "Yet modern engineers admit that achieving this level of geometric symmetry today "
            "would require 3D laser-cutting equipment."
        ),
        "search_term": "Ellora Caves India Pillars at Kailasa Temple"
    },
    {
        "id": 4,
        "narrative": (
            "Even stranger—over 200,000 tons of removed stone debris have vanished completely. "
            "No rubble heaps exist anywhere near Ellora. Where did the mountain go? "
            "Who possessed the ancient technology to hollow out a mountain?"
        ),
        "search_term": "Ellora Cave 16 Kailasa Temple"
    },
    {
        "id": 5,
        "narrative": (
            "The Kailasa Temple stands as timeless proof of India's forgotten master engineers. "
            "Subscribe for more unsolved ancient mysteries, and tell us in the comments—how do you think this monolith was built?"
        ),
        "search_term": "Majestic Kailasa Temple Ellora Aurangabad"
    }
]

# =============================================================================
# STEP 1: VOICE SYNTHESIS (edge-tts)
# =============================================================================
async def generate_scene_audio(scene_id, text):
    audio_path = os.path.join(OUTPUT_DIR, f"audio_{scene_id}.mp3")
    print(f"🎙️ Generating voiceover for Scene {scene_id}...")
    communicate = edge_tts.Communicate(text, VOICE, rate="-3%", pitch="-1Hz")
    await communicate.save(audio_path)
    return audio_path

async def generate_all_audios():
    tasks = [generate_scene_audio(s["id"], s["narrative"]) for s in SCENES]
    return await asyncio.gather(*tasks)

# =============================================================================
# HELPER: SUBTITLE OVERLAY ENGINE
# =============================================================================
def add_subtitles_to_image(image, text, mode="16_9"):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    if mode == "16_9":
        fontsize = 44
        wrap_width = 44
        pos_y = int(h * 0.85)
        font_color = (255, 255, 255)
    else:  # 9:16 Shorts
        fontsize = 52
        wrap_width = 22
        pos_y = int(h * 0.72)
        font_color = (250, 204, 21)  # Vibrant Solar Yellow

    try:
        font = ImageFont.truetype("arialbd.ttf", fontsize)
    except Exception:
        try:
            font = ImageFont.truetype("arial.ttf", fontsize)
        except Exception:
            font = ImageFont.load_default()

    wrapped_text = textwrap.fill(text, width=wrap_width)

    # Text Bounding Box & Pill Background
    bbox = draw.textbbox((w // 2, pos_y), wrapped_text, font=font, anchor="mm", align="center")
    pad_x, pad_y = 25, 15
    pill_box = (bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y)

    draw.rounded_rectangle(pill_box, radius=18, fill=(10, 5, 20))

    # Text Outline
    for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2)]:
        draw.text((w // 2 + dx, pos_y + dy), wrapped_text, font=font, fill=(0, 0, 0), anchor="mm", align="center")

    # Main Text
    draw.text((w // 2, pos_y), wrapped_text, font=font, fill=font_color, anchor="mm", align="center")
    return img

# =============================================================================
# STEP 2: DYNAMIC DUAL-IMAGE FETCHING & SUBTITLE BURNING
# =============================================================================
def fetch_hd_images_for_scenes():
    print("🎨 Fetching HD images from Wikimedia Commons API...")
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": "Kailasa temple Ellora",
        "srnamespace": 6,
        "srlimit": 25,
        "format": "json"
    }
    headers = {"User-Agent": "MegalithicPodcast/1.0 (contact@example.com)"}

    res = requests.get(url, params=params, headers=headers).json()
    results = res.get("query", {}).get("search", [])

    fetched_images = []
    for r in results:
        title = r["title"].replace("File:", "").replace(" ", "_")
        img_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{title}?width=1920"
        try:
            r_img = requests.get(img_url, headers=headers, timeout=12)
            if r_img.status_code == 200:
                img = Image.open(io.BytesIO(r_img.content)).convert("RGB")
                if img.width > 800:
                    fetched_images.append(img)
                    if len(fetched_images) >= len(SCENES) * 2:
                        break
        except Exception:
            pass

    print(f"✅ Downloaded {len(fetched_images)} HD visuals.")

    # Process, crop watermarks, & burn subtitles for each scene
    for idx, scene in enumerate(SCENES):
        sid = scene["id"]
        narration = scene["narrative"]

        img_primary = fetched_images[(idx * 2) % len(fetched_images)]
        img_secondary = fetched_images[(idx * 2 + 1) % len(fetched_images)]

        for img_num, raw_img in enumerate([img_primary, img_secondary], start=1):
            w, h = raw_img.size
            raw_cropped = raw_img.crop((0, 0, w, int(h * 0.94))) # Crop watermark

            # 16:9 Widescreen (1920x1080) with subtitles
            img_16_9 = raw_cropped.resize((1920, 1080), Image.Resampling.LANCZOS)
            img_16_9_sub = add_subtitles_to_image(img_16_9, narration, mode="16_9")
            img_16_9_sub.save(os.path.join(OUTPUT_DIR, f"scene_{sid}_img_{img_num}_16_9.jpg"), quality=95)

            # 9:16 Vertical Shorts (1080x1920) with subtitles
            target_aspect = 9 / 16
            crop_w = int(raw_cropped.height * target_aspect)
            if crop_w < raw_cropped.width:
                left = (raw_cropped.width - crop_w) // 2
                raw_v = raw_cropped.crop((left, 0, left + crop_w, raw_cropped.height))
            else:
                raw_v = raw_cropped

            img_9_16 = raw_v.resize((1080, 1920), Image.Resampling.LANCZOS)
            img_9_16_sub = add_subtitles_to_image(img_9_16, narration, mode="9_16")
            img_9_16_sub.save(os.path.join(OUTPUT_DIR, f"scene_{sid}_img_{img_num}_9_16.jpg"), quality=95)

    print("✂️ Watermarks cropped & animated subtitles burned onto images!")

# =============================================================================
# STEP 3: BUILD VIDEO (WIDESCREEN 16:9 & YOUTUBE SHORTS 9:16)
# =============================================================================
def build_video(mode="16_9", output_mp4=WIDESCREEN_MP4):
    print(f"\n🎬 Assembling {mode} Video Clips with Subtitles & Visual Transitions...")
    scene_clips = []

    for s in SCENES:
        sid = s["id"]
        audio_path = os.path.join(OUTPUT_DIR, f"audio_{sid}.mp3")
        audio_clip = AudioFileClip(audio_path)
        total_dur = audio_clip.duration + 0.3
        half_dur = total_dur / 2.0

        img1_path = os.path.join(OUTPUT_DIR, f"scene_{sid}_img_1_{mode}.jpg")
        img2_path = os.path.join(OUTPUT_DIR, f"scene_{sid}_img_2_{mode}.jpg")

        clip1 = ImageClip(img1_path).with_duration(half_dur)
        clip2 = ImageClip(img2_path).with_duration(total_dur - half_dur)

        scene_visual = concatenate_videoclips([clip1, clip2], method="compose").with_audio(audio_clip)
        scene_clips.append(scene_visual)

    final_video = concatenate_videoclips(scene_clips, method="compose")
    print(f"🚀 Rendering Final Video ({mode}) -> {output_mp4}")
    final_video.write_videofile(
        output_mp4,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="medium"
    )
    print(f"✅ Video Output Ready: {output_mp4}\n")

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    print("=========================================================")
    print("  AI PODCAST & SHORTS GENERATOR (WITH SUBTITLES)        ")
    print("=========================================================\n")

    asyncio.run(generate_all_audios())
    fetch_hd_images_for_scenes()
    build_video(mode="16_9", output_mp4=WIDESCREEN_MP4)
    build_video(mode="9_16", output_mp4=SHORTS_MP4)

    print("=========================================================")
    print("🎉 BOTH SUBTITLED VIDEOS GENERATED & READY ON DESKTOP:")
    print(f"  1. Full Subtitled Video (16:9): {WIDESCREEN_MP4}")
    print(f"  2. Subtitled YouTube Short (9:16): {SHORTS_MP4}")
    print("=========================================================\n")
