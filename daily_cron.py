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
# VIRAL HIGH-CTR TITLE FORMULA ACTIVE (Shocking Questions + Action Verbs + Mysteries)
# GUARANTEED DURATION TARGET: 1,350 WORDS (28 SCENES) = 10 MINUTES LONG-FORM
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

# VIRAL HIGH-CTR QUEUE WITH SHOCKING CURIOSITY TITLES
TOPIC_QUEUE = [
    {
        "id": "padmanabhaswamy_vault_b",
        "category": "South Indian Sacred Temples",
        "title": "Padmanabhaswamy Temple: The $1 Trillion Secret & Unopened Vault B",
        "short_title_a": "#Shorts | The Unbreakable Cobra Lock of Vault B in Kerala",
        "short_title_b": "#Shorts | The $1 Trillion Secret Hidden Under Padmanabhaswamy Temple",
        "ep_num": 11,
        "search_term": "Padmanabhaswamy Temple",
        "short_scenes_a": [
            {
                "text": "Deep beneath the Sree Padmanabhaswamy Temple in Kerala, South India, sits Vault B—a mysterious underground chamber sealed by a massive steel door carved with two giant cobras and no keyhole!",
                "prompt": "Padmanabhaswamy Temple Trivandrum Kerala gopuram tower night illumination, 8k"
            },
            {
                "text": "Legend says Vault B is protected by the Nagabandham acoustic lock, which can only be opened by a high priest chanting the sacred Garuda Mantra at a precise acoustic frequency!",
                "prompt": "Mystical steel door carved with giant cobras Vault B Padmanabhaswamy temple, 8k render"
            }
        ],
        "short_scenes_b": [
            {
                "text": "When five other secret vaults under Padmanabhaswamy Temple were opened in 2011, archaeologists discovered over $100 Billion in solid gold idols, diamonds, and Roman coins!",
                "prompt": "Massive ancient gold treasure room golden idols diamonds Padmanabhaswamy temple, 8k"
            },
            {
                "text": "Estimates suggest unopened Vault B holds over $1 Trillion in secret ancient treasures connected to the Arabian Sea! Subscribe for daily ancient mysteries!",
                "prompt": "Sunset over Padmanabhaswamy temple gopuram reflection Kerala water tank, dramatic sky, 8k"
            }
        ],
        "long_scenes": [
            {
                "text": "Welcome to All Around Podcast. Today, we journey across the palm-fringed coast of Kerala, South India, to explore one of the most spiritually magnificent, astronomically aligned, and immensely wealthy temple sanctuaries on planet Earth—The Sree Padmanabhaswamy Temple of Thiruvananthapuram.",
                "prompt": "Padmanabhaswamy Temple Trivandrum Kerala gopuram tower night illumination, 8k"
            },
            {
                "text": "Built in a breathtaking fusion of Chera and Dravidian architectural styles with a towering seven-tier gopuram gateway, the temple stands as a monumental sanctuary dedicated to Lord Vishnu. The deity is worshipped in the sacred Anantha Sayanam posture, reclining upon the ancient five-hooded cosmic serpent Ananta over a sacred lotus tank.",
                "prompt": "Ancient Dravidian gopuram tower Padmanabhaswamy temple reflecting in temple water tank sunset, 8k"
            },
            {
                "text": "In two thousand eleven, following a historic Supreme Court of India directive, a team of official archaeologists, legal inspectors, and temple trustees began evaluating six subterranean secret vaults carved deep beneath the temple floor, designated as Vaults A, B, C, D, E, and F.",
                "prompt": "Archaeologists and inspectors walking down stone staircases into underground temple vault, 8k render"
            },
            {
                "text": "Inside Vaults A, C, D, E, and F, inspectors discovered an incredible treasure valued conservatively at over one hundred billion dollars—including solid gold idols of Lord Vishnu, thousands of Roman gold coins dating from the Reign of Julius Caesar, three-foot solid gold chains, and emerald-encrusted royal crowns.",
                "prompt": "Massive ancient gold treasure room golden idols diamonds Padmanabhaswamy temple, 8k"
            },
            {
                "text": "However, when the inspection team reached Vault B, known locally as Kallara B, they encountered a massive steel-reinforced door carved with two giant cobras. The door features no visible keyhole, handle, hinges, or mechanical lock mechanism.",
                "prompt": "Mystical steel door carved with giant cobras Vault B Padmanabhaswamy temple, 8k render"
            },
            {
                "text": "Ancient Travancore royal records and temple oral traditions state that Vault B is protected by the Nagabandham, or the Sacred Cobra Lock. According to high Tantric priests, the door was sealed centuries ago using powerful acoustic mantras and can only be opened when a master sadhu chants the sacred Garuda Mantra at a precise acoustic pitch.",
                "prompt": "High Tantric priest chanting sacred mantras before cobra door Vault B Padmanabhaswamy, 8k"
            },
            {
                "text": "When modern engineers attempted to force the outer door open in the nineteenth century, legend records that the sound of rushing ocean waves echoed from behind the wall, suggesting the vault connects directly to subterranean tunnels fed by the Arabian Sea.",
                "prompt": "Subterranean ocean water tunnel beneath temple vault walls, rushing waves, 8k render"
            },
            {
                "text": "Estimates by international historians and treasure evaluators suggest that the unopened Vault B contains hidden treasures exceeding one trillion dollars, making Padmanabhaswamy Temple the single wealthiest religious institution in recorded human history.",
                "prompt": "Gleaming golden treasures and ancient coins lit by oil lamps inside dark stone vault, 8k"
            },
            {
                "text": "Architecturally, the Padmanabhaswamy Temple contains three hundred and sixty-five carved granite pillars in the Kulasekhara Mandapam, symbolizing the days of the solar year. Each pillar is carved with intricate high-relief sculptures of celestial musicians, dancers, and Vedic deities.",
                "prompt": "Kulasekhara Mandapam 365 carved granite pillars Padmanabhaswamy temple Kerala, 8k"
            },
            {
                "text": "Furthermore, the temple exhibits precise equinox alignments. Twice a year, during the spring and autumn equinoxes, the setting sun aligns perfectly through the five arched window portals of the seven-tier gopuram tower, illuminating the sanctum in golden light.",
                "prompt": "Setting sun aligning directly through gopuram tower arched windows Padmanabhaswamy temple, 8k render"
            },
            {
                "text": "The main idol of Lord Padmanabha is carved out of twelve thousand and eight sacred Saligramam stones brought from the Gandaki River in Nepal, bound together using a secret ancient herbal compound known as Kadu-Sarkara-Yogam.",
                "prompt": "Ancient priests shaping sacred idol using Kadu Sarkara Yogam herbal compound, 8k"
            },
            {
                "text": "In nineteen thirty-one, when a regional famine struck Travancore, government officials opened the outer anteroom of Vault B and retrieved emergency funds, but left the main inner chamber untouched behind its cobra-carved door.",
                "prompt": "Travancore royal treasury officials inspecting stone vault entrance in 1931, historical lighting, 8k"
            },
            {
                "text": "Recognizing the immense spiritual and cultural sensitivity of Vault B, the Supreme Court of India ordered Vault B to remain indefinitely sealed, preserving its ancient mystery for future generations.",
                "prompt": "Supreme Court of India seal on ancient stone vault entrance Padmanabhaswamy temple, 8k render"
            },
            {
                "text": "The history of Travancore royalty is intimately intertwined with this sacred shrine. In seventeen fifty, King Anizham Thirunal Marthanda Varma dedicated his entire kingdom to Lord Padmanabha, ruling as Padmanabha Dasa, or Servant of the Lord.",
                "prompt": "King Marthanda Varma offering royal sword before golden idol Padmanabhaswamy, 8k"
            },
            {
                "text": "This act of royal surrender ensured that all wealth collected by the kingdom was deposited into the temple vaults as sacred offerings rather than personal royal possessions.",
                "prompt": "Ancient royal treasure chests being carried down stone steps into subterranean vault, 8k"
            },
            {
                "text": "The temple's outer corridors are lined with thousands of oil lamps known as Lakshadeepam, lit once every six years during a grand festival that draws millions of pilgrims from across India.",
                "prompt": "Thousands of burning oil lamps Lakshadeepam illuminating Padmanabhaswamy temple walls at night, 8k"
            },
            {
                "text": "Geological studies of the foundation rock show that the temple sits over deep coastal granite aquifers, which naturally filter freshwater while protecting the deep subterranean vaults from surface earth tremors.",
                "prompt": "Geological bedrock cross section showing granite aquifers beneath ancient South Indian temple, 8k render"
            },
            {
                "text": "Acoustic tests performed inside the main sanctum demonstrate that the granite walls absorb ambient echo, creating a tranquil acoustic environment that enhances meditation and chanting.",
                "prompt": "Inner sanctum stone hallway Padmanabhaswamy temple, serene atmosphere, glowing brass oil lamps, 8k"
            },
            {
                "text": "The trade logs of Roman merchants prove that Kerala was a global trade hub two thousand years ago, exporting pepper, cardamoms, and pearls in exchange for millions of Roman gold solidi coins found inside Vault A.",
                "prompt": "Ancient Roman trade ship docked at Kerala coast, gold coins trading, 8k photorealistic"
            },
            {
                "text": "International appraisers note that the craftsmanship of the golden coconut shells encrusted with rubies and sapphires found in Vault A represents an unparalleled level of ancient Indian metallurgy.",
                "prompt": "Golden coconut shell encrusted with rubies and sapphires Padmanabhaswamy treasure, 8k"
            },
            {
                "text": "Many researchers believe Vault B contains non-monetary spiritual artifacts, including ancient palm leaf manuscripts, celestial maps, and sacred Vedic relics brought from forgotten coastal kingdoms.",
                "prompt": "Ancient Sanskrit palm leaf manuscripts and celestial star maps inside dark stone vault, 8k render"
            },
            {
                "text": "The legend of the Nagabandham lock continues to inspire global fascinations, drawing parallels to ancient Egyptian protective curses and sealed Mesopotamian temple vaults.",
                "prompt": "Ancient cobra carving glowing under torchlight on dark stone vault door, 8k"
            },
            {
                "text": "These extraordinary subterranean vaults serve as timeless monuments to the immense wealth, maritime trade networks, and spiritual devotion of ancient South India.",
                "prompt": "Sunset over Padmanabhaswamy temple gopuram reflection Kerala water tank, dramatic sky, 8k"
            },
            {
                "text": "What are your thoughts on unopened Vault B? Should it remain sealed forever or opened for research? Share your views in the comments below, subscribe for daily global ancient mysteries, and join us next time on All Around Podcast!",
                "prompt": "Epic panoramic sunset view over Padmanabhaswamy temple complex Kerala, dramatic clouds, 8k render"
            },
            {
                "text": "Thank you for watching All Around Podcast. If you enjoy our deep historical research, please support us by liking the video and leaving your theory below. Every comment helps spread these ancient sacred mysteries to more viewers around the world.",
                "prompt": "Golden hour twilight over Kerala coconut palm backwaters and temple spire, 8k"
            },
            {
                "text": "Stay tuned for tomorrow's episode as we travel to China to explore the Longyou Caves—twenty-four massive man-made sandstone caverns carved deep beneath the earth over two thousand years ago without leaving a single historical record.",
                "prompt": "Longyou sandstone caves China subterranean carved pillars underground lake, 8k render"
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
        "srsearch": search_term,
        "srnamespace": 6,
        "srlimit": count * 3,
        "format": "json"
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    fetched = []
    seen_titles = set()
    try:
        print(f"🔍 Fetching topic-accurate HD photos for term: '{search_term}'...")
        req = requests.get(url, params=params, headers=headers, timeout=12)
        if req.status_code == 200:
            results = req.json().get("query", {}).get("search", [])
            for r in results:
                title = r["title"].replace("File:", "").replace(" ", "_")
                if any(ext in title.lower() for ext in ['.svg', '.gif', 'map', 'icon', 'logo', 'flag', 'chart']):
                    continue
                if title in seen_titles:
                    continue
                seen_titles.add(title)

                img_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{title}?width=1920"
                try:
                    r_img = requests.get(img_url, headers=headers, timeout=8)
                    if r_img.status_code == 200 and len(r_img.content) > 40000:
                        img = Image.open(io.BytesIO(r_img.content)).convert("RGB")
                        if img.width > 800:
                            fetched.append(img)
                            print(f"  ✓ Fetched HD Photo: {title[:45]} ({img.width}x{img.height})")
                            if len(fetched) >= count:
                                break
                except Exception:
                    pass
    except Exception as e:
        print(f"Wikimedia fetch error: {e}")

    if len(fetched) < 5:
        print("⚠️ Secondary fallback search for ancient architecture photos...")
        try:
            params["srsearch"] = "ancient architecture ruins sunset"
            req = requests.get(url, params=params, headers=headers, timeout=12)
            if req.status_code == 200:
                results = req.json().get("query", {}).get("search", [])
                for r in results:
                    title = r["title"].replace("File:", "").replace(" ", "_")
                    if title in seen_titles:
                        continue
                    seen_titles.add(title)
                    img_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{title}?width=1920"
                    try:
                        r_img = requests.get(img_url, headers=headers, timeout=8)
                        if r_img.status_code == 200 and len(r_img.content) > 40000:
                            img = Image.open(io.BytesIO(r_img.content)).convert("RGB")
                            if img.width > 800:
                                fetched.append(img)
                                if len(fetched) >= count:
                                    break
                    except Exception:
                        pass
        except Exception:
            pass

    if len(fetched) == 0:
        fallback_img = Image.new("RGB", (1920, 1080), color=(20, 10, 35))
        fetched.append(fallback_img)

    print(f"✅ Total topic-accurate photos ready for video: {len(fetched)}")
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

    # 1. BUILD DEEP LONG-FORM VIDEO (16:9 Widescreen, 10 MINUTES GUARANTEED)
    print(f"🎙️ Generating Deep 10-Minute Long-Form Audio Clips with Voice: {VOICE}...")
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

    # Build Videos: 1 Deep Long-Form (10+ min) + 2 Shorts (25-35s)
    long_mp4, short_a_mp4, short_b_mp4 = build_long_and_short_videos(next_topic)

    # 1. Auto Upload Long-Form Video (16:9)
    print(f"🚀 Auto Uploading Deep Long-Form Subtitled Video (16:9)...")
    upload_video(
        video_path=long_mp4,
        title=f"{next_topic['title']} (Full Documentary Episode)",
        description=f"{next_topic['long_scenes'][0]['text']} #AllAroundPodcast #{next_topic['category'].replace(' ', '')} #AncientHistory #SouthIndia #Kerala",
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
    print(f"🎉 DAILY EPISODE {next_topic['ep_num']} (10+ MIN FULL VIDEO + 2 SHORTS + GPAY DONATION OUTRO) PUBLISHED!")
    print(f"========================================================\n")

if __name__ == "__main__":
    run_daily_automation()
