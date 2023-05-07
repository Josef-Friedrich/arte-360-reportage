#! /usr/bin/python

import typing


from _lib import geo_360, clean_title
from _youtube import fetch_videos_by_playlist, fetch_videos_by_channel


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

                        episode = geo_360.get_episode_by_title(title, debug=True)
                        if episode:
                            episode["youtube_video_id"] = video_id


merge(fetch_videos_by_channel("UC4W-JsjRBsAvE6DZGOc8LGw"))
merge(fetch_videos_by_playlist("PLAocIS-jUf43CkOnsymOxHihGWKfCkUDC"))

geo_360.save()
