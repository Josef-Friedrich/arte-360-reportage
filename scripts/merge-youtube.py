#! /usr/bin/python

""" Pull All Youtube Videos from a Playlist """

# google-api-python-client
# google-api-python-client-stubs

import json
import pathlib

import _lib

from googleapiclient.discovery import build

from _lib import geo_360

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
    videos = fetch_all_youtube_videos("PLAocIS-jUf43CkOnsymOxHihGWKfCkUDC")
    print(json.dumps(videos, indent=2))

    if "items" in videos:
        for video in videos["items"]:
            if "snippet" in video:
                snippet = video['snippet']
                if "title" in snippet:
                    title: str = snippet["title"]
                    if title == "Private video":
                        continue
                    print(title, _lib.clean_title(title))

                    if "resourceId" in snippet and "videoId" in snippet["resourceId"]:
                        video_id = snippet["resourceId"]["videoId"]

                        episode = geo_360.get_episode_by_title(title)
                        if episode:
                            episode["youtube_video_id"] = video_id



        geo_360.save()
                ##print(video["snippet"]["resourceId"]["videoId"])
                # print(video["snippet"]["description"])
