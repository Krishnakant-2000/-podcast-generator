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

# UNIQUE & TRENDING QUEUE (2,650 WORDS / 23 SCENES PER 18-MIN LONG EPISODE)
TOPIC_QUEUE = [
    {
        "id": "derinkuyu_underground_city",
        "category": "Global Megaliths",
        "title": "Derinkuyu: The 18-Story Subterranean City Built to Survive Cosmic Apocalypse",
        "short_title_a": "Why Did 20,000 People Live 18 Stories Underground in Turkey? #Shorts",
        "short_title_b": "The 1,000-Pound Rolling Stone Doors of Derinkuyu #Shorts #PreFlood",
        "ep_num": 9,
        "search_term": "Derinkuyu underground city Cappadocia Turkey subterranean tunnels",
        "short_scenes_a": [
            {
                "text": "Deep beneath the volcanic plains of Cappadocia, Turkey, sits Derinkuyu—an eighteen-story subterranean city carved two hundred and sixty feet into solid rock, designed to house over twenty thousand people!",
                "prompt": "Derinkuyu underground city Cappadocia Turkey subterranean stone chambers torchlight, 8k"
            },
            {
                "text": "Complete with ventilation shafts, animal stables, wine presses, and chapels, every level could be sealed from within by massive one-thousand-pound rolling stone doors!",
                "prompt": "Massive 1000 lb circular rolling stone door sealing underground tunnel Derinkuyu, 8k render"
            }
        ],
        "short_scenes_b": [
            {
                "text": "Why did an ancient population expend millions of hours carving an eighteen-story bunker beneath the Earth?",
                "prompt": "Subterranean stone staircases winding deep into dark underground city Derinkuyu Turkey, 8k"
            },
            {
                "text": "Geologists believe Derinkuyu was built to shelter humanity from the freezing Younger Dryas cosmic comet impact eleven thousand years ago! Subscribe for daily ancient mysteries!",
                "prompt": "Comet explosion in Earth atmosphere over Cappadocia volcanic peaks Turkey, dramatic 8k"
            }
        ],
        "long_scenes": [
            {
                "text": "Welcome to All Around Podcast. Today, we descend over two hundred and sixty feet beneath the volcanic tuff plains of Cappadocia, Turkey, to explore one of the most astonishing, complex, and urgent subterranean engineering achievements in human history—The Underground City of Derinkuyu.",
                "prompt": "Derinkuyu underground city Cappadocia Turkey subterranean stone chambers torchlight, 8k"
            },
            {
                "text": "Discovered completely by accident in nineteen sixty-three when a local resident knocked down a cellar wall inside his home, Derinkuyu opened into a massive, multi-tiered labyrinth of stone tunnels, living quarters, kitchens, storehouses, and wine presses extending eighteen levels deep into bedrock.",
                "prompt": "Ancient subterranean stone living quarters Derinkuyu Turkey, warm torchlight glow, 8k"
            },
            {
                "text": "Mainstream historical accounts attribute Derinkuyu to the Phrygians in the eighth century BCE or early Byzantine Christians hiding from Roman persecution. However, structural engineers and geologists recognize that the scale and ventilation dynamics of the city reflect a far more ancient, high-capacity engineering effort.",
                "prompt": "Deep vertical stone ventilation shaft Derinkuyu underground city, sunlight beam shining down, 8k"
            },
            {
                "text": "Derinkuyu was not a mere temporary hiding cave. It was a fully self-contained subterranean metropolis designed to comfortably support over twenty thousand human beings, along with thousands of livestock, food reserves, and fresh water supplies for months at a time without anyone needing to surface.",
                "prompt": "Ancient subterranean stone hall Derinkuyu with animal stalls and arched stone pillars, 8k render"
            },
            {
                "text": "The engineering required to carve an eighteen-story city out of soft volcanic tuff rock without causing widespread structural collapses is staggering. Master masons left thick structural bedrock pillars on every single level to distribute the weight of the mountain above.",
                "prompt": "Massive bedrock support pillars in subterranean stone chamber Derinkuyu, dramatic shadows, 8k"
            },
            {
                "text": "To keep twenty thousand people breathing two hundred and sixty feet underground, ancient engineers carved a master vertical air shaft over one hundred and eighty feet deep that functioned as a central atmospheric chimney, connected to over fifteen thousand smaller ventilation ducts.",
                "prompt": "Ancient ventilation duct carved into volcanic rock wall Derinkuyu, fresh air circulation flow diagram, 8k"
            },
            {
                "text": "Fresh water was supplied through subterranean wells that plunged deep into underground aquifers. Crucially, the bottom wells were disconnected from upper levels so invaders on the surface could not poison the drinking water supply.",
                "prompt": "Underground freshwater stone well shaft Derinkuyu subterranean aquifer, crystal clear water, 8k"
            },
            {
                "text": "The defense systems of Derinkuyu are unlike anything seen in surface warfare. Every single level could be isolated and locked independently from the inside using massive five-foot-tall, one-thousand-pound circular rolling stone doors.",
                "prompt": "Massive 1000 lb circular rolling stone door sealing underground tunnel Derinkuyu, 8k render"
            },
            {
                "text": "These giant millstone doors were shaped so they could only be rolled into place from inside the tunnel. A central hole carved through the middle allowed defenders to thrust spears through the sealed door while remaining completely invulnerable to external attack.",
                "prompt": "Close up central spear hole carved in circular rolling stone door Derinkuyu, defender perspective, 8k"
            },
            {
                "text": "Why would an ancient population expend millions of human labor hours excavating tens of thousands of tons of volcanic rock to construct an eighteen-story underground fortress?",
                "prompt": "Subterranean stone staircases winding deep into dark underground city Derinkuyu Turkey, 8k"
            },
            {
                "text": "Mainstream theories claim the city was built for defense against enemy armies. But military strategists point out that hiding twenty thousand people underground with burning torches and animals creates massive smoke, sanitation, and waste hazards that make surface warfare far more practical.",
                "prompt": "Ancient torches glowing along narrow underground stone passageways Derinkuyu, atmospheric haze, 8k"
            },
            {
                "text": "Alternative geologists and researchers like Graham Hancock propose that Derinkuyu was built as a cosmic fallout shelter designed to protect human civilization from an extreme global climate cataclysm—the Younger Dryas comet impact around 10,800 BCE.",
                "prompt": "Comet explosion in Earth atmosphere over Cappadocia volcanic peaks Turkey, dramatic 8k"
            },
            {
                "text": "During the Younger Dryas, a series of cometary fragments struck the Northern Hemisphere, detonating ice sheets, triggering global wildfires, and plunging the planet into a sudden, bitter Ice Age winter lasting twelve hundred years.",
                "prompt": "Global winter ice sheet freezing landscape over ancient Anatolia Turkey, cosmic cataclysm, 8k render"
            },
            {
                "text": "Faced with freezing surface temperatures, intense solar radiation bursts, and torrential meteor fallout, ancient societies built Derinkuyu as a permanent subterranean bunker where human culture, agriculture seeds, and livestock could survive the cosmic winter.",
                "prompt": "Ancient people taking shelter in warm underground stone city Derinkuyu, glowing central hearth fire, 8k"
            },
            {
                "text": "Derinkuyu is not an isolated miracle. Ground-penetrating radar surveys across Cappadocia have discovered over two hundred interconnected underground cities, including Kaymakli, Ozkonak, and the recently discovered Nevsehir subterranean complex.",
                "prompt": "Regional map of Cappadocia showing connected network of 200 underground cities, 8k render"
            },
            {
                "text": "Together, this subterranean network was capable of sheltering over one hundred thousand people beneath the Earth's surface—constituting the largest cataclysm bunker system ever discovered in the ancient world.",
                "prompt": "Panoramic cross section view of 18 story subterranean city Derinkuyu under volcanic plateau, 8k"
            },
            {
                "text": "The sheer scale of Derinkuyu proves that ancient humanity possessed engineering capabilities, atmospheric physics, and geological foresight that rival modern military bunker architecture.",
                "prompt": "Sunlight shining down through main vertical entrance shaft into Derinkuyu underground city, golden rays, 8k"
            },
            {
                "text": "As archaeologists continue to explore only ten percent of this massive subterranean network, Derinkuyu stands as silent physical proof that ancient humans survived a cataclysm that erased surface history.",
                "prompt": "Starry night sky over Cappadocia fairy chimneys volcanic rock landscape Turkey, 8k photorealistic"
            },
            {
                "text": "Was Derinkuyu constructed as an ancient cosmic apocalypse bunker? Share your theories in the comments below, subscribe for daily global ancient mysteries, and join us next time on All Around Podcast!",
                "prompt": "Epic aerial view of Cappadocia volcanic plateau at sunset, dramatic orange sky, 8k render"
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
        images.extend(fetch_wikimedia_hd_images("ancient subterranean city cave sunset", count=45))

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

    # APPEND GPAY DONATION OUTRO TO LONG-FORM VIDEO
    print("💳 Appending GPay Donation Outro to Long-Form Video...")
    gpay_audio_long = asyncio.run(generate_scene_audio("long_gpay", 99, GPAY_DONATION_TEXT))
    gpay_audio_long_clip = AudioFileClip(gpay_audio_long)
    gpay_card_long = generate_gpay_outro_card(mode="16_9")
    gpay_clip_long = ImageClip(gpay_card_long).with_duration(gpay_audio_long_clip.duration + 0.5).with_audio(gpay_audio_long_clip)
    long_clips.append(gpay_clip_long)

    full_long_video = concatenate_videoclips(long_clips, method="compose")
    long_mp4 = os.path.join(LONG_UPLOADS_DIR, f"Daily_Episode_{ep_num}_Long_16_9.mp4")
    print(f"🚀 Rendering Deep Long-Form Video ({full_long_video.duration:.1f}s / {int(full_long_video.duration/60)}m {int(full_long_video.duration%60)}s) -> {long_mp4}")
    full_long_video.write_videofile(long_mp4, fps=24, codec="libx264", audio_codec="aac", preset="medium")

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
    gpay_audio_short_a = asyncio.run(generate_scene_audio("short_a_gpay", 99, GPAY_DONATION_TEXT))
    gpay_audio_short_a_clip = AudioFileClip(gpay_audio_short_a)
    gpay_card_short_a = generate_gpay_outro_card(mode="9_16")
    gpay_clip_short_a = ImageClip(gpay_card_short_a).with_duration(gpay_audio_short_a_clip.duration + 0.3).with_audio(gpay_audio_short_a_clip)
    short_a_clips.append(gpay_clip_short_a)

    full_short_a = concatenate_videoclips(short_a_clips, method="compose")
    short_a_mp4 = os.path.join(SHORTS_UPLOADS_DIR, f"Daily_Episode_{ep_num}_ShortA_9_16.mp4")
    print(f"🚀 Rendering Short Hook A ({full_short_a.duration:.1f}s) -> {short_a_mp4}")
    full_short_a.write_videofile(short_a_mp4, fps=24, codec="libx264", audio_codec="aac", preset="medium")

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
    gpay_audio_short_b = asyncio.run(generate_scene_audio("short_b_gpay", 99, GPAY_DONATION_TEXT))
    gpay_audio_short_b_clip = AudioFileClip(gpay_audio_short_b)
    gpay_card_short_b = generate_gpay_outro_card(mode="9_16")
    gpay_clip_short_b = ImageClip(gpay_card_short_b).with_duration(gpay_audio_short_b_clip.duration + 0.3).with_audio(gpay_audio_short_b_clip)
    short_b_clips.append(gpay_clip_short_b)

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
        description=f"{next_topic['long_scenes'][0]['text']} #AllAroundPodcast #{next_topic['category'].replace(' ', '')} #AncientHistory #Derinkuyu",
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
