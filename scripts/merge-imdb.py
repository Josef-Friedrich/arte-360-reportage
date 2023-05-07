#! /usr/bin/python

import re

import _lib

imdb = _lib.read_text_file("imdb.html")

for found in re.finditer(
    r"<a href=\"/title/(.*?)/.*\".*itemprop=\"name\">(.*)</a>", imdb
):
    episode_id = found.group(1)
    title = found.group(2)

    episode = _lib.geo_360.get_episode_by_title(title, debug=True)
    if episode:
        episode["imdb_episode_id"] = episode_id

_lib.geo_360.save()
