import os
import sys
import json

# =============================================================================
# COMMAND 6: CROSS-PLATFORM SOCIAL THREAD & NEWSLETTER REPURPOSER
# =============================================================================
# Turn script transcript into:
# -> Viral X (Twitter) / Threads summary thread.
# -> Substack / Newsletter edition.
# -> Direct plug for GPay support.

def repurpose_content(topic_title, main_body_text):
    print(f"\n📲 Repurposing Content for X/Threads & Substack: '{topic_title}'...")

    social_data = {
        "topic": topic_title,
        "twitter_thread": [
            f"1/5 🧵 Did a pre-flood global civilization possess high technology before the Younger Dryas cataclysm? Let's break down the evidence from {topic_title} 👇",
            f"2/5 🏛️ Built thousands of years before metal chisels or wheel transport, these massive 100-ton stone blocks fit together with micro-millimeter precision. A razor blade cannot slide between the joints.",
            f"3/5 🎶 Acoustic tests reveal that central stone pillars vibrate at precise harmonic frequencies matching classical Indian musical octaves (432 Hz).",
            f"4/5 🌊 Geological water weathering marks prove rain erosion occurred during prolonged rainy periods prior to 9,000 BCE—thousands of years before mainstream history claims.",
            f"5/5 📺 Watch the full 15-minute documentary episode on YouTube now: All Around Podcast! If you enjoy our research, screenshot our GPay QR to support us via UPI! 🌌"
        ],
        "substack_newsletter": {
            "subject": f"The Lost Pre-Flood Science of {topic_title}",
            "body": (
                f"Welcome to this week's edition of All Around Podcast Newsletter.\n\n"
                f"In today's deep-dive, we examine {topic_title}.\n\n"
                f"Mainstream history teaches that ancient humans were primitive hunter-gatherers until farming began 6,000 years ago. "
                f"Yet carbon dating and geological weathering prove that advanced megalithic architecture existed deep in prehistory...\n\n"
                f"Watch the full 15-minute episode on YouTube and support our independent research via GPay UPI!"
            )
        }
    }

    out_file = os.path.join(os.path.dirname(__file__), "social_repurpose_output.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(social_data, f, indent=2)

    print("✅ X/Threads Thread & Newsletter Edition generated!")
    print("\n🧵 VIRAL X/THREADS THREAD:")
    for tweet in social_data["twitter_thread"]:
        print(f"\n{tweet}")

    print("\n📧 SUBSTACK NEWSLETTER DRAFT:")
    print(f"Subject: {social_data['substack_newsletter']['subject']}")
    print(social_data['substack_newsletter']['body'])

if __name__ == "__main__":
    repurpose_content(
        "Hampi Vittala Temple Musical Pillars",
        "Exploring the 56 solid granite musical pillars of Hampi."
    )
