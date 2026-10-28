import os
import sys
import json

# =============================================================================
# COMMAND 4: HIGH-CTR TITLE & THUMBNAIL MATRIX GENERATOR
# =============================================================================
# Rules:
# -> 10 curiosity-driven titles (fewer than 6 words each).
# -> 3-word thumbnail text options.
# -> COMPLEMENTARITY RULE: Thumbnail text NEVER repeats words from title!
# -> Midjourney / AI visual prompts for high-impact thumbnail art.

def generate_title_matrix(topic_title, topic_details):
    print(f"\n🎯 Generating High-CTR Title & Thumbnail Matrix for: '{topic_title}'...")

    # Complementary Matrix Templates following <6 words title + 3-word non-repeating thumbnail text
    matrix_data = {
        "topic": topic_title,
        "titles_and_thumbnails": [
            {
                "title": "Did 200,000 Tons Just Vanish?",
                "thumbnail_text": "IMP0SSIBLE ROCK CUT",
                "midjourney_prompt": "Cinematic aerial shot of ancient megalithic mountain cut top-down, dramatic golden hour, 8k photorealistic"
            },
            {
                "title": "Built Before Metal Tools Surfaced",
                "thumbnail_text": "11,000 YEARS OLD",
                "midjourney_prompt": "Glowing T-shaped carved stone monolith in desert canyon at twilight, 8k render"
            },
            {
                "title": "The Pre-Flood Sound Generator Mystery",
                "thumbnail_text": "RESONANCE CHAMBER DISCOVERED",
                "midjourney_prompt": "Interior rose granite chamber with glowing acoustic frequency waves, 8k"
            },
            {
                "title": "Why Did They Bury This?",
                "thumbnail_text": "COSMIC FALLOUT SHELTER",
                "midjourney_prompt": "Ground-penetrating radar scanning ancient stone circles buried beneath soil, 8k"
            },
            {
                "text_title": "125-Ton Interlocking Stone Paradox",
                "thumbnail_text": "ZERO MORTAR USED",
                "midjourney_prompt": "Close up polygonal stone wall joints fitted with micro-millimeter precision, 8k"
            },
            {
                "title": "Engineers Sawed It In Half",
                "thumbnail_text": "SOLID GRANITE INSIDE",
                "midjourney_prompt": "Vintage historical British engineers inspecting sawed open stone pillar, 8k"
            },
            {
                "title": "The 18-Story Subterranean City",
                "thumbnail_text": "20,000 PEOPLE HIDDEN",
                "midjourney_prompt": "18 story underground city cavern with rolling stone door, torchlight, 8k"
            },
            {
                "title": "Why Scientists Fear This Stone",
                "thumbnail_text": "MELTED ROCK SURFACES",
                "midjourney_prompt": "Laser-cut vitrified stone cliff reflecting intense solar beam, 8k render"
            },
            {
                "title": "The Floating 52-Ton Magnet",
                "thumbnail_text": "PORTUGUESE SHIPS RUINED",
                "midjourney_prompt": "Ancient temple lodestone attracting metal ship compasses, dramatic sea storm, 8k"
            },
            {
                "title": "Erased From Modern History Books",
                "thumbnail_text": "PRE-FLOOD HIGH TECH",
                "midjourney_prompt": "Ancient map overlaying global megalithic ruins at sunset, 8k"
            }
        ]
    }

    out_file = os.path.join(os.path.dirname(__file__), "title_matrix_output.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(matrix_data, f, indent=2)

    print("✅ High-CTR Title & Thumbnail Matrix generated!")
    for idx, item in enumerate(matrix_data["titles_and_thumbnails"], 1):
        print(f"\n  [{idx}] Title: {item.get('title', item.get('text_title'))}")
        print(f"      Thumbnail Text (3 Words): {item['thumbnail_text']}")
        print(f"      Midjourney Prompt: {item['midjourney_prompt']}")

if __name__ == "__main__":
    generate_title_matrix(
        "Ancient Megalithic Mysteries",
        "Exploring pre-flood high technology, acoustic stone pillars, and Younger Dryas cataclysms."
    )
