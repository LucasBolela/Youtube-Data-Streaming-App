from helpers.playlist.videos.fetch_videos_page import fetch_videos_page


def fetch_videos(google_api_key: str, youtube_playlist_id: str, page_token=None):
    payload = fetch_videos_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_videos(google_api_key, youtube_playlist_id, next_page_token)
