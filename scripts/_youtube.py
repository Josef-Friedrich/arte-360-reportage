#! /usr/bin/python


# google-api-python-client
# google-api-python-client-stubs

import json
import pathlib
import typing


from googleapiclient.discovery import build  # type: ignore


# UC4W-JsjRBsAvE6DZGOc8LGw


# ansible role y/youtube-dl
keys = json.load(open(pathlib.Path.home() / ".youtube-api.json", "r"))
DEVELOPER_KEY = keys["api_key"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


youtube = None


def get_youtube_resource():
    global youtube
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )
    return youtube


def print_json(dump: typing.Any) -> None:
    print(json.dumps(dump, indent=2))


def fetch_videos_by_playlist(playlist_id: str):
    youtube = get_youtube_resource()

    result = (
        youtube.playlistItems()
        .list(part="snippet", playlistId=playlist_id, maxResults=50)
        .execute()
    )

    next_page_token = result.get("nextPageToken")  # type: ignore
    while "nextPageToken" in result:
        if not next_page_token:
            continue
        next_page = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )
        if "items" in result and "items" in next_page:
            result["items"] = result["items"] + next_page["items"]

        if "nextPageToken" not in next_page:
            result.pop("nextPageToken", None)
        else:
            next_page_token: str = next_page["nextPageToken"]

    return result


def get_playlist_id_of_channel(channel_id: str) -> str | None:
    youtube = get_youtube_resource()

    result = youtube.channels().list(part="contentDetails", id=channel_id).execute()

    if "items" in result:
        if len(result["items"]) > 0:
            channel = result["items"][0]
            if "contentDetails" in channel:
                content_details = channel["contentDetails"]
                if "relatedPlaylists" in content_details:
                    related_playlists = content_details["relatedPlaylists"]
                    if "uploads" in related_playlists:
                        return related_playlists["uploads"]


def fetch_videos_by_channel(channel_id: str):
    playlist_id = get_playlist_id_of_channel(channel_id)
    if not playlist_id:
        raise Exception(f"No upload playlist found for channel {channel_id}")
    return fetch_videos_by_playlist(playlist_id)
