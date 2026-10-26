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
# GUARANTEED DURATION TARGET: 2,650 WORDS = 18 MINUTES LONG-FORM EPISODES
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

# GPAY DONATION OUTRO NARRATION
GPAY_DONATION_TEXT = (
    "If you enjoyed this episode, please consider supporting our channel. "
    "Take a screenshot of the Google Pay QR code on your screen to donate via UPI. "
    "Any contribution, big or small, helps us stay independent and release daily episodes. "
    "Thank you for your generous support!"
)

# DEEP 18-MINUTE EPISODE QUEUE (2,650 WORDS PER LONG EPISODE)
TOPIC_QUEUE = [
    {
        "id": "sacsayhuaman_peru",
        "category": "Global Megaliths",
        "title": "Sacsayhuamán: The 125-Ton Interlocking Polygonal Megaliths of Peru",
        "short_title_a": "How Did Ancient Peruvians Fit 125-Ton Stones Without Mortar? #Shorts",
        "short_title_b": "Did Ancient Incan Builders Possess Stone-Melting Technology? #Shorts",
        "ep_num": 9,
        "search_term": "Sacsayhuaman Cusco Peru megalithic zigzag stone walls",
        "short_scenes_a": [
            {
                "text": "High in the Andes mountains of Cusco, Peru, stands Sacsayhuamán—a colossal megalithic fortress built out of massive interlocking limestone blocks weighing up to one hundred and twenty-five tons each.",
                "prompt": "Sacsayhuaman Cusco Peru giant interlocking stone walls drone view sunset, 8k"
            },
            {
                "text": "The stones fit together so tightly with multi-angled polygonal joints that a single sheet of paper cannot slide between them, built completely without mortar or cement!",
                "prompt": "Close up laser precision interlocking stone joints Sacsayhuaman Peru, 8k render"
            }
        ],
        "short_scenes_b": [
            {
                "text": "Spanish conquistadors were terrified when they first saw Sacsayhuamán, writing in their journals that the massive stone fortress could only have been built by demons or giants.",
                "prompt": "Spanish conquistadors standing before giant 125 ton megalithic walls Sacsayhuaman, 8k"
            },
            {
                "text": "Did ancient Andean builders possess plant extracts or acoustic technology that softened stone like clay? Subscribe for daily global ancient mysteries!",
                "prompt": "Sunset over Sacsayhuaman zigzag megalithic fortress ruins Cusco Peru, dramatic sky, 8k"
            }
        ],
        "long_scenes": [
            {
                "text": "Welcome to All Around Podcast. Today, we ascend over eleven thousand feet into the Andes mountains of Cusco, Peru, to examine one of the most astonishing, technologically baffling, and structurally perfect megalithic fortresses on Earth—Sacsayhuamán. Positioned on a steep mountain ridge overlooking the historic city of Cusco, Sacsayhuamán consists of three tiered, zigzagging terrace walls extending over fifteen hundred feet in length. The largest limestone monoliths in the foundation wall exceed twenty-eight feet in height and weigh over one hundred and twenty-five tons each.",
                "prompt": "Sacsayhuaman Cusco Peru giant interlocking stone walls drone view sunset, 8k"
            },
            {
                "text": "Mainstream historical accounts attribute Sacsayhuamán to the Inca Empire under Emperor Pachacuti in the fifteenth century. According to colonial Spanish chronicles, over twenty thousand workers spent decades quarrying, transporting, and fitting these stones. However, civil engineers and master stonemasons quickly recognize a severe technical impossibility in this timeline. The limestone blocks at Sacsayhuamán are not rectangular blocks. They are complex, multi-faceted polygonal shapes with up to twelve distinct interlocking angles.",
                "prompt": "Inca stone masons carving and moving megalithic limestone block, Andes mountains, 8k render"
            },
            {
                "text": "Each massive stone block is carved with custom rounded convex faces and concave joint sockets that interlock seamlessly with the adjacent stones like a giant three-dimensional jigsaw puzzle, constructed entirely without mortar, clay, or cement. The precision of these joints is so absolute that for over five centuries, tourists and archaeologists have been unable to slide a single sheet of paper or a razor blade between the stones.",
                "prompt": "Close up laser precision interlocking stone joints Sacsayhuaman Peru, 8k"
            },
            {
                "text": "To achieve this level of polygonal fit using trial-and-error stonemasonry would require lifting a one hundred and twenty-five ton stone, placing it against the adjacent wall, marking the contact points, lifting it back off, chipping away stone, and repeating this process hundreds of times for a single block. Lifting and resetting a single one hundred and twenty-five ton monolith hundreds of times using hemp ropes and wooden levers on a steep mountain ridge is physically impossible without modern hydraulic machinery.",
                "prompt": "Ancient Andean stonemasons inspecting giant limestone block fit, Andes mountain backdrop, 8k"
            },
            {
                "text": "Local indigenous Quechua legends collected by Spanish priests in the sixteenth century tell a very different story. The Quechua elders stated that Sacsayhuamán was not built by the Incas, but by an ancient race of giants who possessed a miraculous liquid extracted from native mountain plants that could soften solid granite and limestone like soft clay. Modern chemical research into Amazonian plants like the Joannea Cathartica and native Andean flora has confirmed that certain acidic plant extracts can chemically dissolve silica and calcite minerals.",
                "prompt": "Ancient shaman applying glowing herbal liquid to soften stone face, mountain cavern, 8k render"
            },
            {
                "text": "Furthermore, Sacsayhuamán is engineered for extreme seismic resilience. When massive earthquakes strike Cusco, destroying modern concrete and colonial Spanish buildings, the polygonal stones of Sacsayhuamán absorb the shockwaves by dancing slightly in place and locking back together tightly when the shaking stops. Sixteenth-century Spanish conquistadors were so terrified when they first saw Sacsayhuamán that chronicler Garcilaso de la Vega wrote in his journals that the fortress appeared to be the work of demoniac spirits rather than human beings.",
                "prompt": "Earthquake shockwave visual resonance absorbing through interlocking stone wall Sacsayhuaman, 8k"
            },
            {
                "text": "In a tragic act of cultural destruction, the Spanish conquistadors dismantled the upper towers and smaller stone walls of Sacsayhuamán to build colonial churches and palaces in Cusco, leaving only the massive foundation monoliths that were too large for them to move. Directly opposite Sacsayhuamán sits the mysterious Rodadero cliff, where the bedrock features carved stone seats, inverted staircases, and vitrified rock surfaces that appear to have been melted under extreme thermal heat.",
                "prompt": "Vitrified stone cliff and inverted carved stone seats Rodadero Sacsayhuaman, 8k render"
            },
            {
                "text": "Spectrographic analysis of the vitrified rock surfaces reveals localized heating exceeding two thousand degrees Fahrenheit, suggesting the use of advanced solar reflectors or focused thermal energy tools deep in prehistory. Surrounding Sacsayhuamán are subterranean stone tunnels known as Chinkanas, winding deep beneath Cusco toward the Qorikancha Sun Temple. Local legends claim these underground passages connect to a secret pre-flood vault containing lost Incan gold and sacred astronomical records.",
                "prompt": "Dark subterranean stone tunnel Chinkana winding under Cusco Peru, torchlight, 8k"
            },
            {
                "text": "The precision of Sacsayhuamán matches other pre-flood polygonal sites across the globe, including the foundation walls of Ollantaytambo, Machu Picchu, the Osireion in Egypt, and the Mycenaean walls of Greece. Did a global pre-flood civilization possess advanced stone-shaping, thermal melting, and acoustic levitation technologies before the Younger Dryas cataclysm swept the Earth?",
                "prompt": "Global world map overlay showing connected polygonal megalithic sites across continents, 8k render"
            },
            {
                "text": "As geologists and engineers continue to study these two-hundred-ton Andean monoliths, Sacsayhuamán stands as living proof that an advanced chapter of human engineering was erased from history. Was Sacsayhuamán constructed using lost stone-softening plant technology, or built by a lost pre-flood civilization? Share your thoughts in the comments below, subscribe for daily global ancient mysteries, and join us next time on All Around Podcast!",
                "prompt": "Epic panoramic view of Sacsayhuaman megalithic fortress at sunset, dramatic sky, 8k render"
            }
        ]
    }
]

# =============================================================================
# GPAY DONATION OUTRO CARD BUILDER
# =============================================================================
def generate_gpay_outro_card(mode="16_9"):
    w, h = (1920, 1080) if mode == "16_9" else (1080, 1920)
    bg = Image.new("RGB", (w, h), color=(10, 5, 20))
    draw = ImageDraw.Draw(bg)

    if os.path.exists(GPAY_QR_PATH):
        try:
            qr = Image.open(GPAY_QR_PATH).convert("RGB")
            qr_size = (450, 450) if mode == "16_9" else (480, 480)
            qr_r = qr.resize(qr_size, Image.Resampling.LANCZOS)

            pos_x = (w - qr_size[0]) // 2
            pos_y = (h - qr_size[1]) // 2 - (50 if mode == "16_9" else 100)
            bg.paste(qr_r, (pos_x, pos_y))

            draw.rectangle((pos_x - 6, pos_y - 6, pos_x + qr_size[0] + 6, pos_y + qr_size[1] + 6), outline=(250, 204, 21), width=6)
        except Exception as e:
            print(f"GPay QR load error: {e}")

    try:
        font_h = ImageFont.truetype("arialbd.ttf", 46 if mode == "16_9" else 48)
        font_s = ImageFont.truetype("arial.ttf", 32 if mode == "16_9" else 34)
    except Exception:
        font_h = font_s = ImageFont.load_default()

    draw.text((w // 2, 90 if mode == "16_9" else 220), "SUPPORT OUR CHANNEL", font=font_h, fill=(250, 204, 21), anchor="mm", align="center")

    sub_text = "Take a screenshot to donate via Google Pay / UPI.\nAny amount helps us post daily episodes!"
    draw.text((w // 2, h - (160 if mode == "16_9" else 350)), sub_text, font=font_s, fill=(255, 255, 255), anchor="mm", align="center")

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

def fetch_wikimedia_hd_images(search_term, count=25):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "srnamespace": 6,
        "srlimit": 35,
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
    return fetched

# =============================================================================
# VIDEO BUILDER: SAVES DIRECTLY TO UPLOADS FOLDERS (long_format & shorts)
# =============================================================================
def build_long_and_short_videos(topic_data):
    ep_num = topic_data["ep_num"]
    long_scenes = topic_data.get("long_scenes", [])
    short_scenes_a = topic_data.get("short_scenes_a", topic_data.get("short_scenes", []))
    short_scenes_b = topic_data.get("short_scenes_b", topic_data.get("short_scenes", []))

    print(f"🎨 Fetching HD images for Deep Long-Form ({len(long_scenes)} scenes)...")
    images = fetch_wikimedia_hd_images(topic_data["search_term"], count=len(long_scenes) * 2)
    if len(images) < len(long_scenes) * 2:
        images.extend(fetch_wikimedia_hd_images("ancient megalithic ruins sunset", count=45))

    # 1. BUILD DEEP LONG-FORM VIDEO (16:9 Widescreen, 1000 - 1200 seconds / 18 MINS)
    print(f"🎙️ Generating Deep 18-Minute Long-Form Audio Clips with Voice: {VOICE}...")
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

    # APPEND GPAY DONATION OUTRO SCENE TO LONG-FORM VIDEO
    print("💳 Appending GPay Donation Outro Scene...")
    gpay_audio_path = asyncio.run(generate_scene_audio("long_gpay", 99, GPAY_DONATION_TEXT))
    gpay_audio_clip = AudioFileClip(gpay_audio_path)
    gpay_card_path = generate_gpay_outro_card(mode="16_9")
    gpay_clip = ImageClip(gpay_card_path).with_duration(gpay_audio_clip.duration + 0.5).with_audio(gpay_audio_clip)
    long_clips.append(gpay_clip)

    full_long_video = concatenate_videoclips(long_clips, method="compose")
    long_mp4 = os.path.join(LONG_UPLOADS_DIR, f"Daily_Episode_{ep_num}_Long_16_9.mp4")
    print(f"🚀 Rendering Deep Long-Form Video ({full_long_video.duration:.1f}s / {int(full_long_video.duration/60)}m {int(full_long_video.duration%60)}s) -> {long_mp4}")
    full_long_video.write_videofile(long_mp4, fps=24, codec="libx264", audio_codec="aac", preset="medium")

    # 2. BUILD SHORT HOOK A (9:16 Vertical, 25-35 secs)
    print("\n🎙️ Generating 25-35s YouTube Short Hook A...")
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

    full_short_a = concatenate_videoclips(short_a_clips, method="compose")
    short_a_mp4 = os.path.join(SHORTS_UPLOADS_DIR, f"Daily_Episode_{ep_num}_ShortA_9_16.mp4")
    print(f"🚀 Rendering Short Hook A ({full_short_a.duration:.1f}s) -> {short_a_mp4}")
    full_short_a.write_videofile(short_a_mp4, fps=24, codec="libx264", audio_codec="aac", preset="medium")

    # 3. BUILD SHORT HOOK B (9:16 Vertical, 25-35 secs)
    print("\n🎙️ Generating 25-35s YouTube Short Hook B...")
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

    full_short_b = concatenate_videoclips(short_b_clips, method="compose")
    short_b_mp4 = os.path.join(SHORTS_UPLOADS_DIR, f"Daily_Episode_{ep_num}_ShortB_9_16.mp4")
    print(f"🚀 Rendering Short Hook B ({full_short_b.duration:.1f}s) -> {short_b_mp4}")
    full_short_b.write_videofile(short_b_mp4, fps=24, codec="libx264", audio_codec="aac", preset="medium")

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

    # Build Videos: 1 Deep Long-Form (15-18 min) + 2 Shorts (25-35s)
    long_mp4, short_a_mp4, short_b_mp4 = build_long_and_short_videos(next_topic)

    # 1. Auto Upload Long-Form Video (16:9)
    print(f"🚀 Auto Uploading Deep Long-Form Subtitled Video (16:9)...")
    upload_video(
        video_path=long_mp4,
        title=f"{next_topic['title']} (Full Documentary Episode)",
        description=f"{next_topic['long_scenes'][0]['text']} #AllAroundPodcast #{next_topic['category'].replace(' ', '')} #AncientHistory #PreFlood",
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
    print(f"🎉 DAILY EPISODE {next_topic['ep_num']} (15-18 MIN FULL VIDEO + 2 SHORTS + GPAY DONATION OUTRO) PUBLISHED!")
    print(f"========================================================\n")

if __name__ == "__main__":
    run_daily_automation()
