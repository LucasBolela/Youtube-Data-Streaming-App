import json
import logging
import requests


def fetch_videos_page(google_api_key: str, video_id: str, page_token=None) -> json:
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={
            "key": google_api_key,
            "id": video_id,
            "part": "snippet,statistics",
            "pageToken": page_token,
        },
    )

    payload = json.loads(response.text)

    logging.debug("GOT %s", payload)

    return payload
