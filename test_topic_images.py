import requests
import io
from PIL import Image

def fetch_topic_images(search_term, count=10):
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

    req = requests.get(url, params=params, headers=headers, timeout=12)
    if req.status_code == 200:
        results = req.json().get("query", {}).get("search", [])
        print(f"\n🔍 Found {len(results)} Wikimedia results for term: '{search_term}'")
        for r in results:
            title = r["title"].replace("File:", "").replace(" ", "_")
            # Skip non-photo graphics, maps, SVG icons
            if any(ext in title.lower() for ext in ['.svg', '.png', '.gif', 'map', 'icon', 'logo', 'flag']):
                continue
            img_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{title}?width=1920"
            try:
                r_img = requests.get(img_url, headers=headers, timeout=8)
                if r_img.status_code == 200 and len(r_img.content) > 50000:
                    img = Image.open(io.BytesIO(r_img.content)).convert("RGB")
                    if img.width > 800:
                        fetched.append((title, img))
                        print(f"  ✓ Fetched HD Topic Image: {title[:50]} ({img.width}x{img.height})")
                        if len(fetched) >= count:
                            break
            except Exception as e:
                pass
    return fetched

if __name__ == "__main__":
    for topic in ["Padmanabhaswamy Temple", "Vittala Temple Hampi", "Derinkuyu underground city", "Sacsayhuaman Cusco"]:
        imgs = fetch_topic_images(topic, count=5)
        print(f"✅ Total unique topic-accurate images for '{topic}': {len(imgs)}")
