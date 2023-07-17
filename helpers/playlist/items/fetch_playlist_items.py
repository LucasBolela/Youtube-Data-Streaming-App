from helpers.playlist.items.fetch_playlist_items_page import fetch_playlist_items_page


def fetch_playlist_items(
    google_api_key: str, youtube_playlist_id: str, page_token=None
):
    payload = fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_playlist_items(
            google_api_key, youtube_playlist_id, next_page_token
        )
