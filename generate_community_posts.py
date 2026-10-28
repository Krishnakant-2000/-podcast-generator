import os
import sys
import json

# =============================================================================
# COMMAND 5: AUTOMATED YOUTUBE COMMUNITY POLLS & PINNED COMMENT GENERATOR
# =============================================================================
# Outputs:
# -> 3 engaging polls for YouTube Community Tab (for non-upload days).
# -> Pinned comment script directing viewers to GPay support link.
# -> High-ranking SEO tags & keywords.

def generate_community_system(topic_title, topic_details):
    print(f"\n📊 Generating Community Polls & Pinned Comment for: '{topic_title}'...")

    community_data = {
        "topic": topic_title,
        "pinned_comment": (
            "👇 Which ancient theory do you believe most? Drop your thoughts below!\n\n"
            "💬 If you enjoy our daily documentary episodes, take a screenshot of the GPay QR code "
            "at the end of the video to donate via UPI. Your support helps us stay independent! 🌌"
        ),
        "seo_tags": [
            "AncientHistory", "Megaliths", "PreFlood", "YoungerDryas",
            "LostCivilization", "Archaeology", "AllAroundPodcast", "Documentary"
        ],
        "community_polls": [
            {
                "poll_number": 1,
                "question": "How do you think ancient megaliths like Göbekli Tepe & Sacsayhuamán were built?",
                "options": [
                    "Acoustic levitation / Frequency resonance 🎶",
                    "Stone-softening plant extracts 🌿",
                    "Lost pre-flood machine technology ⚙️",
                    "Manual slave labor & wooden ramps 🪵"
                ]
            },
            {
                "poll_number": 2,
                "question": "Was the Great Pyramid of Giza originally constructed as a Tomb or a Power Plant?",
                "options": [
                    "Piezoelectric Acoustic Power Plant ⚡",
                    "Astronomical Pre-Flood Vault 🌌",
                    "Pharaoh Khufu's Burial Tomb 👑",
                    "Chemical Hydrogen Reaction Cell 🧪"
                ]
            },
            {
                "poll_number": 3,
                "question": "Which ancient site should we investigate in our next 15-minute documentary?",
                "options": [
                    "Derinkuyu 18-Story Underground City (Turkey) 🇹🇷",
                    "Padmanabhaswamy Temple Vault B Door (India) 🇮🇳",
                    "Longyou Caves 24 Sandstone Caverns (China) 🇨🇳",
                    "Puma Punku Diorite H-Blocks (Bolivia) 🇧🇴"
                ]
            }
        ]
    }

    out_file = os.path.join(os.path.dirname(__file__), "community_posts_output.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(community_data, f, indent=2)

    print("✅ YouTube Community Polls & Pinned Comment generated!")
    print("\n📌 PINNED COMMENT SCRIPT:")
    print(community_data["pinned_comment"])

    print("\n🗳️ COMMUNITY TAB POLLS (For Non-Upload Days):")
    for poll in community_data["community_polls"]:
        print(f"\n Poll #{poll['poll_number']}: {poll['question']}")
        for opt in poll["options"]:
            print(f"  - {opt}")

if __name__ == "__main__":
    generate_community_system(
        "Ancient Megalithic Mysteries",
        "Exploring pre-flood high technology and acoustic stone pillars."
    )
