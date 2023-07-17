import json
import logging
import requests


def fetch_playlist_items_page(
    google_api_key: str, youtube_playlist_id: str, page_token=None
) -> json:
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/playlistItems",
        params={
            "key": google_api_key,
            "playlistId": youtube_playlist_id,
            "part": "contentDetails",
            "pageToken": page_token,
        },
    )

    payload = json.loads(response.text)

    logging.debug("GOT %s", payload)

    return payload
