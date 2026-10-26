import os
import sys
import pickle
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# =============================================================================
# YOUTUBE OAUTH & SCOPES CONFIGURATION
# =============================================================================
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_PICKLE_FILE = os.path.join(os.path.dirname(__file__), "token.pickle")

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"❌ ERROR: Missing '{CLIENT_SECRETS_FILE}'!")
                print("Please download client_secret.json from Google Cloud Console and place it in the ai_podcast_generator folder.")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(TOKEN_PICKLE_FILE, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

# =============================================================================
# YOUTUBE UPLOAD FUNCTION
# =============================================================================
def upload_video(video_path, title, description, tags=None, category_id="27", privacy="public"):
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        return None

    if tags is None:
        tags = ["Ancient Mysteries", "Kailasa Temple", "Ellora Caves", "Indian History", "Archeology", "Shorts"]

    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title[:100],  # YouTube title limit 100 chars
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")

    print(f"\n🚀 Initiating YouTube Upload for: {os.path.basename(video_path)}")
    print(f"📌 Title: {title}")
    print(f"🔒 Privacy Status: {privacy}\n")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"⏳ Upload progress: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"\n🎉 SUCCESS! Video uploaded to YouTube!")
    print(f"👉 Watch Live Video: {video_url}\n")
    return video_url

# =============================================================================
# MAIN CLI EXECUTION
# =============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload AI generated podcast videos to YouTube")
    parser.add_argument("--video", required=True, help="Path to MP4 video file")
    parser.add_argument("--title", required=True, help="YouTube Video Title")
    parser.add_argument("--desc", default="Unsolved Ancient Megalithic Mysteries of India. Subscribe for more history secrets!", help="Video Description")
    parser.add_argument("--privacy", default="public", choices=["public", "private", "unlisted"], help="Video privacy")

    args = parser.parse_args()
    upload_video(args.video, args.title, args.desc, privacy=args.privacy)
