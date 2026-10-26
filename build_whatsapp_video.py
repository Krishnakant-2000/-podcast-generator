import os
import sys
import textwrap
import asyncio
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips

# =============================================================================
# INPUT PATHS & OUTPUT CONFIGURATION
# =============================================================================
RAW_VIDEO_PATH = r"C:\Users\USER\Desktop\IMG_0154.MP4"
LOGO_PATH = r"C:\Users\USER\Desktop\images and ss\logo.png"

OUT_ENGLISH_MP4 = r"C:\Users\USER\Desktop\WhatsApp_AmaPlayer_Demo_English.mp4"
OUT_HINDI_MP4 = r"C:\Users\USER\Desktop\WhatsApp_AmaPlayer_Demo_Hindi.mp4"

# NARRATION SCRIPTS
ENG_NARRATION = (
    "Welcome to AmaPlayer. Score any live match ball-by-ball, goal-by-goal, or point-by-point! "
    "Every match you score automatically syncs to your profile, building your official sports career records! "
    "View your Player Stats Card, track your accuracy, and climb the Scout Score Leaderboard! "
    "Download AmaPlayer free today on Play Store and App Store!"
)

HINDI_NARRATION = (
    "AmaPlayer में आपका स्वागत है। किसी भी मैच का बॉल-बाय-बॉल, गोल या अंक का लाइव स्कोर करें! "
    "हर मैच का स्कोर आपके प्रोफ़ाइल से जुड़ता है, जिससे आपका आधिकारिक स्पोर्ट्स करियर रिकॉर्ड बनता है! "
    "अपना प्लेयर कार्ड देखें, अपनी सटीकता ट्रैक करें और स्काउट स्कोर लीडरबोर्ड पर आगे बढ़ें! "
    "आज ही प्ले स्टोर और ऐप स्टोर से मुफ़्त में AmaPlayer डाउनलोड करें!"
)

# =============================================================================
# HELPER: OUTRO CTA CARD WITH LOGO
# =============================================================================
def create_outro_card(lang="en"):
    bg = Image.new("RGB", (1080, 1920), color=(10, 5, 20))
    draw = ImageDraw.Draw(bg)

    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            lw, lh = logo.size
            target_w = 420
            target_h = int(lh * (target_w / lw))
            logo_r = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
            bg.paste(logo_r, (1080 // 2 - target_w // 2, 1920 // 2 - 380), mask=logo_r)
        except Exception as e:
            print("Logo load error:", e)

    try:
        font_h = ImageFont.truetype("arialbd.ttf", 56)
        font_s = ImageFont.truetype("arial.ttf", 38)
    except Exception:
        font_h = font_s = ImageFont.load_default()

    if lang == "en":
        head_text = "DOWNLOAD NOW"
        sub_text = "Available Free on\nPlay Store & App Store"
    else:
        head_text = "अभी डाउनलोड करें"
        sub_text = "प्ले स्टोर और ऐप स्टोर पर\nमुफ़्त उपलब्ध है"

    draw.text((1080 // 2, 1920 // 2 + 120), head_text, font=font_h, fill=(250, 204, 21), anchor="mm", align="center")
    draw.text((1080 // 2, 1920 // 2 + 220), sub_text, font=font_s, fill=(255, 255, 255), anchor="mm", align="center")

    out_file = os.path.join(os.path.dirname(__file__), f"temp_whatsapp_outro_{lang}.jpg")
    bg.save(out_file, quality=95)
    return out_file

# =============================================================================
# MAIN VIDEO PROCESSOR
# =============================================================================
async def gen_audio(text, voice, out_path):
    c = edge_tts.Communicate(text, voice, rate="-2%", pitch="-1Hz")
    await c.save(out_path)

def build_whatsapp_video(lang="en", output_path=OUT_ENGLISH_MP4):
    print(f"\n🎬 Building Perfectly Synchronized Video ({lang.upper()})...")

    narration_text = ENG_NARRATION if lang == "en" else HINDI_NARRATION
    voice = "en-GB-RyanNeural" if lang == "en" else "hi-IN-SwaraNeural"
    audio_path = os.path.join(os.path.dirname(__file__), f"temp_whatsapp_audio_{lang}.mp3")

    asyncio.run(gen_audio(narration_text, voice, audio_path))
    narration_audio = AudioFileClip(audio_path)

    # Load raw video
    raw_clip = VideoFileClip(RAW_VIDEO_PATH)

    # STRICT FRAME CUTS:
    # 1. Live Badminton Scoring Action (0s to 11.2s) -> CUTS BEFORE EXIT WARNING POPUP
    c1 = raw_clip.subclipped(0, 11.2)

    # 2. User Profile & Track Records (28.8s to 37.0s) -> JUMPS DIRECTLY TO PROFILE
    c2 = raw_clip.subclipped(28.8, 37.0)

    # 3. Player Stats Card (38.0s to 45.0s) -> STATS CARD & LEADERBOARD
    c3 = raw_clip.subclipped(38.0, 45.0)

    # Concatenate clean video segments (Zero warning popup!)
    clean_demo = concatenate_videoclips([c1, c2, c3]).resized(new_size=(1080, 1920))

    # Outro CTA Clip
    outro_card_img = create_outro_card(lang)
    outro_clip = ImageClip(outro_card_img).with_duration(4.5)

    # Combine demo and outro
    final_video_visual = concatenate_videoclips([clean_demo, outro_clip], method="compose")

    # Sync narration audio
    final_video = final_video_visual.with_duration(narration_audio.duration).with_audio(narration_audio)

    print(f"🚀 Rendering Final Video ({final_video.duration:.1f}s) -> {output_path}")
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        ffmpeg_params=["-pix_fmt", "yuv420p"]
    )

    raw_clip.close()
    narration_audio.close()
    print(f"✅ Finished & Saved: {output_path}\n")

if __name__ == "__main__":
    build_whatsapp_video(lang="en", output_path=OUT_ENGLISH_MP4)
    build_whatsapp_video(lang="hi", output_path=OUT_HINDI_MP4)
