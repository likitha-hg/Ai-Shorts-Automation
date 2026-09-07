import os
import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

PEXELS_URL = "https://api.pexels.com/videos/search"

headers = {
    "Authorization": PEXELS_API_KEY
}


def get_stock_video(scene: str, output_path: str):

    if not PEXELS_API_KEY:
        raise Exception("PEXELS_API_KEY not found")

    os.makedirs("output", exist_ok=True)

    response = requests.get(
        PEXELS_URL,
        headers=headers,
        params={
            "query": scene,
            "per_page": 1
        },
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(
            f"Pexels API Error ({response.status_code}): {response.text}"
        )

    data = response.json()

    videos = data.get("videos", [])

    if not videos:
        raise Exception(f"No stock video found for scene: {scene}")

    # Pick best quality clip
    video_files = videos[0].get("video_files", [])

    if not video_files:
        raise Exception("No downloadable video files found")

    best_video = sorted(
        video_files,
        key=lambda x: x.get("width", 0),
        reverse=True
    )[0]

    video_url = best_video["link"]

    video_response = requests.get(
        video_url,
        timeout=120
    )

    if video_response.status_code != 200:
        raise Exception("Failed to download stock video")

    with open(output_path, "wb") as f:
        f.write(video_response.content)

    return output_path