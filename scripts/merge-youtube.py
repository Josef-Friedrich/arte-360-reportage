#! /usr/bin/python

import typing

from _lib import clean_title, tv_show
from _youtube import fetch_videos_by_channel, fetch_videos_by_playlist


def merge(playlist_items: typing.Any):
    if "items" in playlist_items:
        for video in playlist_items["items"]:
            if "snippet" in video:
                snippet = video["snippet"]
                if "title" in snippet:
                    title: str = snippet["title"]
                    if title == "Private video":
                        continue
                    title = clean_title(title)

                    if "resourceId" in snippet and "videoId" in snippet["resourceId"]:
                        video_id = snippet["resourceId"]["videoId"]

                        episode = tv_show.get_episode_by_title(title, debug=True)
                        if episode:
                            episode["youtube_video_id"] = video_id


merge(fetch_videos_by_channel("UC4W-JsjRBsAvE6DZGOc8LGw"))
merge(fetch_videos_by_playlist("PLAocIS-jUf43CkOnsymOxHihGWKfCkUDC"))

tv_show.save()
