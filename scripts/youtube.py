#! /usr/bin/python

""" Pull All Youtube Videos from a Playlist """

# google-api-python-client
# google-api-python-client-stubs

from googleapiclient.discovery import build

import pathlib
import json


# ansible role y/youtube-dl
p = pathlib.Path.home() / ".youtube-api.json"
keys = json.load(open(p, "r"))
DEVELOPER_KEY = keys["api_key"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def fetch_all_youtube_videos(playlistId: str):
    """
    Fetches a playlist of videos from youtube
    We splice the results together in no particular order

    Parameters:
        parm1 - (string) playlistId
    Returns:
        playListItem Dict
    """
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
    )
    result = (
        youtube.playlistItems()
        .list(part="snippet", playlistId=playlistId, maxResults=50)
        .execute()
    )

    nextPageToken = result.get("nextPageToken")
    while "nextPageToken" in result:
        nextPage = (
            youtube.playlistItems()
            .list(
                part="snippet",
                playlistId=playlistId,
                maxResults=50,
                pageToken=nextPageToken,
            )
            .execute()
        )
        result["items"] = result["items"] + nextPage["items"]

        if "nextPageToken" not in nextPage:
            result.pop("nextPageToken", None)
        else:
            nextPageToken = nextPage["nextPageToken"]

    return result


if __name__ == "__main__":
    # comedy central playlist, has 332 video
    # https://www.youtube.com/watch?v=tJDLdxYKh3k&list=PLD7nPL1U-R5rDpeH95XsK0qwJHLTS3tNT
    videos = fetch_all_youtube_videos("PLD7nPL1U-R5rDpeH95XsK0qwJHLTS3tNT")

    print(json.dumps(videos, indent=2))
