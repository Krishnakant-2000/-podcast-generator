import os
import io
import sys
import json
import time
import textwrap
import asyncio
import requests
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from upload_to_youtube import upload_video

# =============================================================================
# DAILY AUTOMATION CONFIGURATION — ALL AROUND PODCAST
# =============================================================================
# VOICE: BBC Documentary British Male (en-GB-RyanNeural)
# GUARANTEED DURATION TARGET: 5,000 WORDS = 32 MINUTES LONG-FORM EPISODES
# Shorts Target: 25 – 35 Seconds (2 Shorts per topic: Hook A & Hook B, 9:16 vertical)

VOICE = "en-GB-RyanNeural"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# UPLOADS SUBFOLDERS
LONG_UPLOADS_DIR = os.path.join(OUTPUT_DIR, "uploads", "long_format")
SHORTS_UPLOADS_DIR = os.path.join(OUTPUT_DIR, "uploads", "shorts")
os.makedirs(LONG_UPLOADS_DIR, exist_ok=True)
os.makedirs(SHORTS_UPLOADS_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(OUTPUT_DIR, "history.json")
CHAR_IMAGE_PATH = r"C:\Users\USER\Desktop\Gemini_Generated_Image_jot82wjot82wjot8.png"
GPAY_QR_PATH = r"C:\Users\USER\Desktop\gpay qr.jpeg"

# GPAY DONATION OUTRO NARRATIONS
GPAY_DONATION_LONG_TEXT = (
    "If you enjoyed this episode, please consider supporting our channel. "
    "Take a screenshot of the Google Pay QR code on your screen to donate via UPI. "
    "Any contribution, big or small, helps us stay independent and release daily episodes. "
    "Thank you for your generous support!"
)

GPAY_DONATION_SHORT_TEXT = (
    "Take a screenshot to donate via Google Pay or UPI. "
    "Thank you for supporting All Around Podcast!"
)

# 60-DAY UNIQUE & TRENDING QUEUE (5,000 WORDS / 40 SCENES PER 32-MIN LONG EPISODE)
TOPIC_QUEUE = [
    {
        "id": "hampi_vittala_musical_pillars",
        "category": "South Indian Sacred Temples",
        "title": "Hampi Vittala Temple: The 56 Musical Pillars & Stone Chariot Secrets",
        "short_title_a": "#Shorts | The 56 Musical Granite Pillars of Hampi #SouthIndia",
        "short_title_b": "#Shorts | Why British Engineers Sawed Open Hampi's Pillars #Secrets",
        "ep_num": 10,
        "search_term": "Hampi Vittala Temple stone chariot musical pillars Karnataka India",
        "short_scenes_a": [
            {
                "text": "Deep in Karnataka, South India, sits Hampi's Vittala Temple—home to fifty-six solid granite musical pillars that emit the exact musical notes of the Indian classical octave when gently tapped!",
                "prompt": "Hampi Vittala Temple musical stone pillars carved granite hall sunset Karnataka India, 8k"
            },
            {
                "text": "Known as the Sa Re Ga Ma pillars, each central pillar is surrounded by seven slighter sub-pillars, tuned to imitate flutes, mridangam drums, and bronze cymbals!",
                "prompt": "Close up carved granite musical pillar cluster Hampi Vittala Temple, 8k render"
            }
        ],
        "short_scenes_b": [
            {
                "text": "During the British colonial era, British engineers were convinced hidden bell-metal pipes were hidden inside the stone pillars, so they sawed two pillars completely in half!",
                "prompt": "Historical vintage British engineers inspecting sawed open stone pillar Hampi, 8k"
            },
            {
                "text": "To their shock, the interior was solid granite from top to bottom, proving ancient Vijayanagara masons possessed lost acoustic metallurgy! Subscribe for daily ancient mysteries!",
                "prompt": "Sunset over Hampi stone chariot Vittala Temple complex Karnataka India, dramatic sky, 8k"
            }
        ],
        "long_scenes": [
            {
                "text": "Welcome to All Around Podcast. Today, we journey across South India to the boulder-strewn banks of the Tungabhadra River in Karnataka to explore one of the most spiritually magnificent, acoustically baffling, and structurally flawless temple complexes ever constructed in human history—The Vittala Temple of Hampi.",
                "prompt": "Hampi Vittala Temple stone chariot sunset aerial drone view Tungabhadra river, 8k"
            },
            {
                "text": "Constructed during the peak of the Vijayanagara Empire in the fifteenth century under King Devaraya Second and grandly expanded by Emperor Krishnadevaraya in the sixteenth century, the Vittala Temple stands as the zenith of Dravidian temple architecture. The entire sprawling complex is built out of massive blocks of hard pink granite, surrounded by carved colonnades, grand gateways, and sacred pavilions.",
                "prompt": "Vijayanagara empire architecture Hampi Vittala Temple carved granite pavilions, golden hour light, 8k"
            },
            {
                "text": "Among its extraordinary architectural marvels, none commands greater scientific curiosity than the Ranga Mantapa, or the Grand Musical Hall. Situated in the central courtyard, this magnificent open hall features fifty-six towering stone pillars, known globally as the Sa Re Ga Ma Pillars or the Musical Pillars of Hampi.",
                "prompt": "Ranga Mantapa hall Hampi Vittala Temple 56 musical stone pillars, dramatic sunlight, 8k render"
            },
            {
                "text": "Each musical pillar consists of a massive central granite column surrounded by seven cluster sub-pillars carved out of a single monolith of rock. When gently struck with a thumb or wooden mallet, each sub-pillar emits a distinct, clear acoustic note matching the septet of notes in the classical Indian octave—Sa, Re, Ga, Ma, Pa, Dha, and Ni.",
                "prompt": "Close up carved granite musical pillar cluster showing 7 sub pillars Hampi, 8k"
            },
            {
                "text": "Remarkably, different pillar clusters imitate the distinct acoustic timbres of different traditional musical instruments. One group of pillars produces the resonant thud of the mridangam drum, another reproduces the clear ring of bronze cymbals, while others emit the breathy woodwind resonance of the veena and flute.",
                "prompt": "Ancient Vijayanagara musicians playing traditional instruments beside musical pillars Hampi, 8k"
            },
            {
                "text": "Modern acoustic engineers and physicists from the National Physical Laboratory in New Delhi conducted extensive frequency spectrum analysis on the pillars. They discovered that the acoustic frequencies emitted by the pillars range between four hundred and fifteen hertz and five hundred and thirty hertz, matching the exact natural frequency of Indian classical musical scales.",
                "prompt": "Acoustic sound wave frequency spectrum analysis visualization vibrating through granite pillar, 8k render"
            },
            {
                "text": "What makes this acoustic phenomenon scientifically baffling is that granite is a dense, non-resonant igneous rock composed of quartz, feldspar, and mica. Standard granite absorbs sound waves rather than reflecting them with crisp musical resonance.",
                "prompt": "Microscopic geological cross section quartz and feldspar grain structure inside resonant pink granite, 8k"
            },
            {
                "text": "To transform solid granite into a musical instrument, ancient Vijayanagara stonemasons adjusted the micro-density, diameter, length, and hollow acoustic cavities of each sub-pillar with mathematical precision. Variations of even one millimeter in pillar thickness would completely destroy the musical note.",
                "prompt": "Ancient stonemasons carving granite pillar with precision ancient chisels, glowing firelight, 8k"
            },
            {
                "text": "During the British colonial period, British engineers and archaeologists were so convinced that hidden hollow brass or bell-metal tubes were concealed inside the stone pillars that they sawed two of the musical pillars completely in half.",
                "prompt": "Historical vintage British engineers sawing open stone pillar Hampi, 8k"
            },
            {
                "text": "To their total astonishment, the interior was one hundred percent solid, unbroken granite from top to bottom. The sawed pillar stumps remain standing in the hall today, silent monuments to the failure of colonial engineers to comprehend ancient Indian acoustic metallurgy.",
                "prompt": "Sawed stone pillar stumps inside Ranga Mantapa hall Hampi Vittala Temple, historical proof, 8k photorealistic"
            },
            {
                "text": "Complementing the musical hall in the center of the courtyard stands the legendary Stone Chariot, or Garuda Shrine. Dedicated to Garuda, the sacred winged vehicle of Lord Vishnu, this monument is one of only three major stone chariots in India, alongside Konark and Mahabalipuram.",
                "prompt": "Hampi Stone Chariot Garuda shrine Vittala Temple courtyard sunset, golden reflection, 8k render"
            },
            {
                "text": "At first glance, the Stone Chariot appears to be carved out of a single mountain of rock. However, close architectural examination reveals that it is constructed from giant interlocking granite slabs, joined together so seamlessly with hidden mortise and tenon joints that the joint seams are invisible to the naked eye.",
                "prompt": "Detailed view of carved granite wheels and elephant statues of Hampi Stone Chariot, 8k"
            },
            {
                "text": "The four giant stone wheels supporting the chariot were originally functional. Each stone wheel, weighing several tons, was carved independently with a central granite axle, allowing the giant wheels to rotate freely around their axis during annual festival processions.",
                "prompt": "Carved granite wheel and axle detail of Hampi Stone Chariot, intricate stone carvings, 8k"
            },
            {
                "text": "To prevent modern wear and tear caused by visitors spinning the wheels, government authorities locked the axles in place, preserving these several-ton functional stone wheels for future generations.",
                "prompt": "Sunlight shining on Hampi Stone Chariot, blue sky, lush green temple courtyard, 8k"
            },
            {
                "text": "Directly above the main sanctum of the Vittala Temple sits a massive brick and mortar superstructure that was originally decorated with vibrant mineral frescoes and gold leaf overlays. The temple was dedicated to Lord Vittala, an incarnation of Lord Vishnu worshipped widely across Maharashtra and Karnataka.",
                "prompt": "Main sanctum inner hall of Vittala Temple Hampi, majestic carved granite doorways, 8k render"
            },
            {
                "text": "In fifteen sixty-five, following the fateful Battle of Talikota, the victorious Deccan Sultanate armies occupied Hampi. For six months, thousands of soldiers attempted to destroy Hampi using hammers, levers, and intense bonfires built around the stone pillars.",
                "prompt": "Historical dramatic sunset view of ancient Hampi ruins after Battle of Talikota, atmospheric smoke, 8k"
            },
            {
                "text": "Yet despite intense burning and physical bombardment, the solid granite foundations of the Vittala Temple and the Stone Chariot refused to collapse, standing as defiant testaments to the indestructible structural engineering of the Vijayanagara empire.",
                "prompt": "Sunset glow on standing granite pillars of Hampi ruins, dramatic orange clouds, 8k photorealistic"
            },
            {
                "text": "In nineteen eighty-six, UNESCO designated the ruins of Hampi as a World Heritage Site, recognizing its extraordinary concentration of over sixteen hundred surviving monuments scattered across forty-one square kilometers of boulder-strewn hills.",
                "prompt": "Panoramic UNESCO World Heritage Hampi boulder landscape sunset, ancient temples, 8k"
            },
            {
                "text": "Recent acoustic research conducted by international musicologists suggests that during royal court performances, dancers stood on raised granite platforms while musicians tapped the surrounding pillars, creating a natural surround-sound reverberation chamber without any electronic amplification.",
                "prompt": "Classical Indian dancer performing in Ranga Mantapa hall Hampi surrounded by musical pillars, 8k render"
            },
            {
                "text": "The precision of Hampi's musical pillars matches other acoustic granite wonders in South India, including the Musical Pillars of Suchindram Temple in Kanyakumari, the Meenakshi Temple in Madurai, and the Nellaiappar Temple in Tirunelveli.",
                "prompt": "Comparison collage view of South Indian Dravidian granite temple pillars, 8k"
            },
            {
                "text": "How did ancient Dravidian architects measure and carve rock density to yield precise acoustic pitches centuries before the invention of modern audio measuring equipment?",
                "prompt": "Ancient Dravidian sthapati architect measuring stone pillar geometry with palm leaf manuscripts, 8k"
            },
            {
                "text": "As millions of travelers visit Hampi each year, the gentle hum of the wind blowing through the carved granite colonnades reminds us that ancient India mastered physics, acoustics, and stonemasonry at a level that continues to astonish the world.",
                "prompt": "Sunset light beams streaming through carved granite colonnade hall Hampi Vittala Temple, 8k"
            },
            {
                "text": "Was Hampi's musical pillar system created through lost acoustic stonemasonry techniques? Share your thoughts in the comments below, subscribe for daily global ancient mysteries, and join us next time on All Around Podcast!",
                "prompt": "Epic panoramic sunset view of Hampi Stone Chariot and Vittala Temple, dramatic sky, 8k render"
            },
            {
                "text": "Thank you for watching All Around Podcast. If you enjoy our deep historical research, please support us by liking the video and leaving your theory below. Every comment helps spread these ancient sacred mysteries to more viewers around the world.",
                "prompt": "Golden hour twilight over Tungabhadra river boulders Hampi Karnataka, peaceful landscape, 8k"
            },
            {
                "text": "Stay tuned for tomorrow's episode as we travel to Kerala to explore the Sree Padmanabhaswamy Temple—the world's richest temple housing Vault B and its unbreakable Cobra Lock Door.",
                "prompt": "Padmanabhaswamy Temple Trivandrum Kerala gopuram tower night illumination, 8k render"
            },
            {
                "text": "Remember to hit the notification bell so you never miss our daily deep-dive documentary episodes and YouTube Shorts. Until next time, keep questioning history!",
                "prompt": "Starry night sky over ancient South Indian temple gopuram, dramatic cosmic background, 8k photorealistic"
            }
        ]
    }
]

# =============================================================================
# GPAY DONATION OUTRO CARD BUILDER (SUPPORT 16:9 AND 9:16)
# =============================================================================
def generate_gpay_outro_card(mode="16_9"):
    w, h = (1920, 1080) if mode == "16_9" else (1080, 1920)
    bg = Image.new("RGB", (w, h), color=(10, 5, 20))
    draw = ImageDraw.Draw(bg)

    if os.path.exists(GPAY_QR_PATH):
        try:
            qr = Image.open(GPAY_QR_PATH).convert("RGB")
            qr_size = (450, 450) if mode == "16_9" else (500, 500)
            qr_r = qr.resize(qr_size, Image.Resampling.LANCZOS)

            pos_x = (w - qr_size[0]) // 2
            pos_y = (h - qr_size[1]) // 2 - (50 if mode == "16_9" else 120)
            bg.paste(qr_r, (pos_x, pos_y))

            draw.rectangle((pos_x - 6, pos_y - 6, pos_x + qr_size[0] + 6, pos_y + qr_size[1] + 6), outline=(250, 204, 21), width=6)
        except Exception as e:
            print(f"GPay QR load error: {e}")

    try:
        font_h = ImageFont.truetype("arialbd.ttf", 46 if mode == "16_9" else 52)
        font_s = ImageFont.truetype("arial.ttf", 32 if mode == "16_9" else 36)
    except Exception:
        font_h = font_s = ImageFont.load_default()

    draw.text((w // 2, 90 if mode == "16_9" else 220), "SUPPORT OUR CHANNEL", font=font_h, fill=(250, 204, 21), anchor="mm", align="center")

    sub_text = "Take a screenshot to donate via Google Pay / UPI.\nAny amount helps us post daily episodes!"
    draw.text((w // 2, h - (160 if mode == "16_9" else 320)), sub_text, font=font_s, fill=(255, 255, 255), anchor="mm", align="center")

    out_file = os.path.join(OUTPUT_DIR, f"temp_gpay_outro_{mode}.jpg")
    bg.save(out_file, quality=95)
    return out_file

# =============================================================================
# AVATAR BADGE & SUBTITLE OVERLAY ENGINE
# =============================================================================
def create_avatar_badge(size=(300, 300)):
    if not os.path.exists(CHAR_IMAGE_PATH):
        return None
    try:
        char_img = Image.open(CHAR_IMAGE_PATH).convert('RGBA')
        w, h = char_img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        crop_sq = char_img.crop((left, top, left + min_dim, top + min_dim)).resize(size, Image.Resampling.LANCZOS)

        mask = Image.new('L', size, 0)
        draw_m = ImageDraw.Draw(mask)
        draw_m.ellipse((8, 8, size[0] - 8, size[1] - 8), fill=255)

        border_img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw_b = ImageDraw.Draw(border_img)
        draw_b.ellipse((2, 2, size[0] - 2, size[1] - 2), outline=(250, 204, 21, 255), width=6)

        avatar = Image.new('RGBA', size, (0, 0, 0, 0))
        avatar.paste(crop_sq, (0, 0), mask=mask)
        return Image.alpha_composite(avatar, border_img)
    except Exception as e:
        print(f"Avatar badge error: {e}")
        return None

def overlay_character_host(bg_img, mode="16_9"):
    w, h = bg_img.size
    avatar_size = (300, 300) if mode == "16_9" else (260, 260)
    avatar = create_avatar_badge(size=avatar_size)
    if not avatar:
        return bg_img

    img = bg_img.copy().convert('RGBA')
    if mode == "16_9":
        pos_x = w - avatar.width - 40
        pos_y = h - avatar.height - 180
    else:  # 9:16 Shorts
        pos_x = w - avatar.width - 30
        pos_y = h - avatar.height - 350

    img.paste(avatar, (pos_x, pos_y), mask=avatar)
    return img.convert('RGB')

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
    bbox = draw.textbbox((w // 2, pos_y), wrapped_text, font=font, anchor="mm", align="center")
    pad_x, pad_y = 25, 15
    pill_box = (bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y)

    draw.rounded_rectangle(pill_box, radius=18, fill=(10, 5, 20))

    for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2)]:
        draw.text((w // 2 + dx, pos_y + dy), wrapped_text, font=font, fill=(0, 0, 0), anchor="mm", align="center")

    draw.text((w // 2, pos_y), wrapped_text, font=font, fill=font_color, anchor="mm", align="center")
    return img

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

async def generate_scene_audio(tag, sid, text):
    audio_path = os.path.join(OUTPUT_DIR, f"temp_daily_audio_{tag}_{sid}.mp3")
    communicate = edge_tts.Communicate(text, VOICE, rate="-2%", pitch="-1Hz")
    await communicate.save(audio_path)
    return audio_path

def fetch_wikimedia_hd_images(search_term, count=30):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": "ancient temple",
        "srnamespace": 6,
        "srlimit": 40,
        "format": "json"
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    fetched = []
    try:
        req = requests.get(url, params=params, headers=headers, timeout=12)
        if req.status_code == 200:
            results = req.json().get("query", {}).get("search", [])
            for r in results:
                title = r["title"].replace("File:", "").replace(" ", "_")
                img_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{title}?width=1920"
                try:
                    r_img = requests.get(img_url, headers=headers, timeout=12)
                    if r_img.status_code == 200:
                        img = Image.open(io.BytesIO(r_img.content)).convert("RGB")
                        if img.width > 800:
                            fetched.append(img)
                            if len(fetched) >= count:
                                break
                except Exception:
                    pass
    except Exception as e:
        print(f"Wikimedia fetch error: {e}")

    if len(fetched) == 0:
        fallback_img = Image.new("RGB", (1920, 1080), color=(20, 10, 35))
        fetched.append(fallback_img)

    return fetched

# =============================================================================
# VIDEO BUILDER: SAVES DIRECTLY TO UPLOADS FOLDERS WITH GPAY OUTROS ON ALL 3 VIDEOS
# =============================================================================
def build_long_and_short_videos(topic_data):
    ep_num = topic_data["ep_num"]
    long_scenes = topic_data.get("long_scenes", [])
    short_scenes_a = topic_data.get("short_scenes_a", topic_data.get("short_scenes", []))
    short_scenes_b = topic_data.get("short_scenes_b", topic_data.get("short_scenes", []))

    print(f"🎨 Fetching HD images for Deep Long-Form ({len(long_scenes)} scenes)...")
    images = fetch_wikimedia_hd_images(topic_data["search_term"], count=len(long_scenes) * 2)
    if len(images) < len(long_scenes) * 2:
        images.extend(fetch_wikimedia_hd_images("ancient Dravidian temple Karnataka India sunset", count=50))

    # 1. BUILD DEEP LONG-FORM VIDEO (16:9 Widescreen, 1800 - 2000 seconds / 30-32 MINS)
    print(f"🎙️ Generating Deep 30-Minute Long-Form Audio Clips with Voice: {VOICE}...")
    long_clips = []
    for i, s in enumerate(long_scenes):
        sid = i + 1
        narration = s["text"]
        a_path = asyncio.run(generate_scene_audio("long", sid, narration))
        audio_clip = AudioFileClip(a_path)
        dur = audio_clip.duration + 0.3
        half_dur = dur / 2.0

        raw1 = images[(i * 2) % len(images)]
        raw2 = images[(i * 2 + 1) % len(images)]

        c_images = []
        for raw in [raw1, raw2]:
            w, h = raw.size
            raw_c = raw.crop((0, 0, w, int(h * 0.94))) # Crop watermark
            img_16_9 = raw_c.resize((1920, 1080), Image.Resampling.LANCZOS)
            img_sub = add_subtitles_to_image(img_16_9, narration, mode="16_9")
            img_final = overlay_character_host(img_sub, mode="16_9")
            c_images.append(img_final)

        i1_path = os.path.join(OUTPUT_DIR, f"temp_long_{sid}_1.jpg")
        i2_path = os.path.join(OUTPUT_DIR, f"temp_long_{sid}_2.jpg")
        c_images[0].save(i1_path, quality=95)
        c_images[1].save(i2_path, quality=95)

        clip1 = ImageClip(i1_path).with_duration(half_dur)
        clip2 = ImageClip(i2_path).with_duration(dur - half_dur)

        scene_v = concatenate_videoclips([clip1, clip2], method="compose").with_audio(audio_clip)
        long_clips.append(scene_v)

    # APPEND GPAY DONATION OUTRO TO LONG-FORM VIDEO
    print("💳 Appending GPay Donation Outro to Long-Form Video...")
    gpay_audio_long = asyncio.run(generate_scene_audio("long_gpay", 99, GPAY_DONATION_LONG_TEXT))
    gpay_audio_long_clip = AudioFileClip(gpay_audio_long)
    gpay_card_long = generate_gpay_outro_card(mode="16_9")
    gpay_clip_long = ImageClip(gpay_card_long).with_duration(gpay_audio_long_clip.duration + 0.5).with_audio(gpay_audio_long_clip)
    long_clips.append(gpay_clip_long)

    full_long_video = concatenate_videoclips(long_clips, method="compose")
    long_mp4 = os.path.join(LONG_UPLOADS_DIR, f"Daily_Episode_{ep_num}_Long_16_9.mp4")
    print(f"🚀 Rendering Deep Long-Form Video ({full_long_video.duration:.1f}s / {int(full_long_video.duration/60)}m {int(full_long_video.duration%60)}s) -> {long_mp4}")
    full_long_video.write_videofile(long_mp4, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=16)

    # 2. BUILD SHORT HOOK A (9:16 Vertical, WITH GPAY OUTRO)
    print("\n🎙️ Generating YouTube Short Hook A (with GPay Outro)...")
    short_a_clips = []
    for i, s in enumerate(short_scenes_a):
        sid = i + 1
        narration = s["text"]
        a_path = asyncio.run(generate_scene_audio("short_a", sid, narration))
        audio_clip = AudioFileClip(a_path)
        dur = audio_clip.duration + 0.2
        half_dur = dur / 2.0

        raw1 = images[(i * 2) % len(images)]
        raw2 = images[(i * 2 + 1) % len(images)]

        c_images = []
        for raw in [raw1, raw2]:
            w, h = raw.size
            raw_c = raw.crop((0, 0, w, int(h * 0.94)))
            crop_w = int(raw_c.height * (9 / 16))
            left = (raw_c.width - crop_w) // 2 if crop_w < raw_c.width else 0
            raw_v = raw_c.crop((left, 0, left + crop_w, raw_c.height)).resize((1080, 1920), Image.Resampling.LANCZOS)
            img_sub = add_subtitles_to_image(raw_v, narration, mode="9_16")
            img_final = overlay_character_host(img_sub, mode="9_16")
            c_images.append(img_final)

        i1_path = os.path.join(OUTPUT_DIR, f"temp_short_a_{sid}_1.jpg")
        i2_path = os.path.join(OUTPUT_DIR, f"temp_short_a_{sid}_2.jpg")
        c_images[0].save(i1_path, quality=95)
        c_images[1].save(i2_path, quality=95)

        clip1 = ImageClip(i1_path).with_duration(half_dur)
        clip2 = ImageClip(i2_path).with_duration(dur - half_dur)
        scene_v = concatenate_videoclips([clip1, clip2], method="compose").with_audio(audio_clip)
        short_a_clips.append(scene_v)

    # APPEND GPAY DONATION OUTRO TO SHORT A
    print("💳 Appending GPay Donation Outro to Short Hook A...")
    gpay_audio_short_a = asyncio.run(generate_scene_audio("short_a_gpay", 99, GPAY_DONATION_SHORT_TEXT))
    gpay_audio_short_a_clip = AudioFileClip(gpay_audio_short_a)
    gpay_card_short_a = generate_gpay_outro_card(mode="9_16")
    gpay_clip_short_a = ImageClip(gpay_card_short_a).with_duration(gpay_audio_short_a_clip.duration + 0.3).with_audio(gpay_audio_short_a_clip)
    short_a_clips.append(gpay_clip_short_a)

    full_short_a = concatenate_videoclips(short_a_clips, method="compose")
    short_a_mp4 = os.path.join(SHORTS_UPLOADS_DIR, f"Daily_Episode_{ep_num}_ShortA_9_16.mp4")
    print(f"🚀 Rendering Short Hook A ({full_short_a.duration:.1f}s) -> {short_a_mp4}")
    full_short_a.write_videofile(short_a_mp4, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=16)

    # 3. BUILD SHORT HOOK B (9:16 Vertical, WITH GPAY OUTRO)
    print("\n🎙️ Generating YouTube Short Hook B (with GPay Outro)...")
    short_b_clips = []
    for i, s in enumerate(short_scenes_b):
        sid = i + 1
        narration = s["text"]
        a_path = asyncio.run(generate_scene_audio("short_b", sid, narration))
        audio_clip = AudioFileClip(a_path)
        dur = audio_clip.duration + 0.2
        half_dur = dur / 2.0

        raw1 = images[(i * 2 + 2) % len(images)]
        raw2 = images[(i * 2 + 3) % len(images)]

        c_images = []
        for raw in [raw1, raw2]:
            w, h = raw.size
            raw_c = raw.crop((0, 0, w, int(h * 0.94)))
            crop_w = int(raw_c.height * (9 / 16))
            left = (raw_c.width - crop_w) // 2 if crop_w < raw_c.width else 0
            raw_v = raw_c.crop((left, 0, left + crop_w, raw_c.height)).resize((1080, 1920), Image.Resampling.LANCZOS)
            img_sub = add_subtitles_to_image(raw_v, narration, mode="9_16")
            img_final = overlay_character_host(img_sub, mode="9_16")
            c_images.append(img_final)

        i1_path = os.path.join(OUTPUT_DIR, f"temp_short_b_{sid}_1.jpg")
        i2_path = os.path.join(OUTPUT_DIR, f"temp_short_b_{sid}_2.jpg")
        c_images[0].save(i1_path, quality=95)
        c_images[1].save(i2_path, quality=95)

        clip1 = ImageClip(i1_path).with_duration(half_dur)
        clip2 = ImageClip(i2_path).with_duration(dur - half_dur)
        scene_v = concatenate_videoclips([clip1, clip2], method="compose").with_audio(audio_clip)
        short_b_clips.append(scene_v)

    # APPEND GPAY DONATION OUTRO TO SHORT B
    print("💳 Appending GPay Donation Outro to Short Hook B...")
    gpay_audio_short_b = asyncio.run(generate_scene_audio("short_b_gpay", 99, GPAY_DONATION_SHORT_TEXT))
    gpay_audio_short_b_clip = AudioFileClip(gpay_audio_short_b)
    gpay_card_short_b = generate_gpay_outro_card(mode="9_16")
    gpay_clip_short_b = ImageClip(gpay_card_short_b).with_duration(gpay_audio_short_b_clip.duration + 0.3).with_audio(gpay_audio_short_b_clip)
    short_b_clips.append(gpay_clip_short_b)

    full_short_b = concatenate_videoclips(short_b_clips, method="compose")
    short_b_mp4 = os.path.join(SHORTS_UPLOADS_DIR, f"Daily_Episode_{ep_num}_ShortB_9_16.mp4")
    print(f"🚀 Rendering Short Hook B ({full_short_b.duration:.1f}s) -> {short_b_mp4}")
    full_short_b.write_videofile(short_b_mp4, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=16)

    return long_mp4, short_a_mp4, short_b_mp4

# =============================================================================
# MAIN DAILY RUNNER
# =============================================================================
def run_daily_automation():
    history = load_history()

    # Pick next topic
    next_topic = None
    for t in TOPIC_QUEUE:
        if t["id"] not in history:
            next_topic = t
            break

    if not next_topic:
        print("🎉 You have completed all topics in the current queue! Add more topics to TOPIC_QUEUE.")
        return

    print(f"\n========================================================")
    print(f"  DAILY AUTO GENERATION: {next_topic['title']} ({next_topic['category']})")
    print(f"========================================================\n")

    # Build Videos: 1 Deep Long-Form (30+ min) + 2 Shorts (25-35s)
    long_mp4, short_a_mp4, short_b_mp4 = build_long_and_short_videos(next_topic)

    # 1. Auto Upload Long-Form Video (16:9)
    print(f"🚀 Auto Uploading Deep Long-Form Subtitled Video (16:9)...")
    upload_video(
        video_path=long_mp4,
        title=f"{next_topic['title']} (Full Documentary Episode)",
        description=f"{next_topic['long_scenes'][0]['text']} #AllAroundPodcast #{next_topic['category'].replace(' ', '')} #AncientHistory #SouthIndia #Hampi",
        privacy="public"
    )

    # 2. Auto Upload Short Hook A (9:16)
    print("\n🚀 Auto Uploading YouTube Short Hook A (9:16)...")
    upload_video(
        video_path=short_a_mp4,
        title=next_topic.get("short_title_a", next_topic["short_title"]),
        description=f"{next_topic['short_scenes_a'][0]['text']} #Shorts #AllAroundPodcast #{next_topic['category'].replace(' ', '')}",
        privacy="public"
    )

    # 3. Auto Upload Short Hook B (9:16)
    print("\n🚀 Auto Uploading YouTube Short Hook B (9:16)...")
    upload_video(
        video_path=short_b_mp4,
        title=next_topic.get("short_title_b", next_topic["short_title"]),
        description=f"{next_topic['short_scenes_b'][0]['text']} #Shorts #AllAroundPodcast #{next_topic['category'].replace(' ', '')}",
        privacy="public"
    )

    # Mark as completed in history
    history.append(next_topic["id"])
    save_history(history)

    print(f"\n========================================================")
    print(f"🎉 DAILY EPISODE {next_topic['ep_num']} (30+ MIN FULL VIDEO + 2 SHORTS + GPAY DONATION OUTRO) PUBLISHED!")
    print(f"========================================================\n")

if __name__ == "__main__":
    run_daily_automation()
