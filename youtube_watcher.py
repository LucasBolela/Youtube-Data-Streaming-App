#!/usr/bin/env python3

import logging
from pprint import pformat
import sys
from config import config
from helpers import on_delivery
from helpers.playlist import fetch_playlist_items
from helpers.playlist.videos import fetch_videos

from helpers.summarize_video import summarize_video

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka import SerializingProducer


def main():
    logging.info("Start")

    schema_registry_client = SchemaRegistryClient(config["schema_registry"])
    youtube_videos_value_schema = schema_registry_client.get_latest_version(
        "youtube_videos-value"
    )

    kafka_config = config.get("kafka") | {
        "key.serializer": StringSerializer(),
        "value.serializer": AvroSerializer(
            schema_registry_client, youtube_videos_value_schema.schema.schema_str
        ),
    }
    producer = SerializingProducer(kafka_config)

    google_api_key = config.get("google_api_key")
    youtube_playlist_id = config.get("youtube_playlist_id")

    for video_item in fetch_playlist_items(google_api_key, youtube_playlist_id):
        video_id = video_item["contentDetails"]["videoId"]
        for video in fetch_videos(google_api_key, video_id):
            logging.info("GOT %s", pformat(summarize_video(video)))

            producer.produce(
                topic="youtube_videos",
                key=video_id,
                value={
                    "TITLE": video["snippet"]["title"],
                    "VIEWS": int(video["statistics"].get("viewCount"), 0),
                    "LIKES": int(video["statistics"].get("likeCount"), 0),
                    "COMMENTS": int(video["statistics"].get("commentCount"), 0),
                },
                on_delivery=on_delivery,
            )

    producer.flush()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
