#! /usr/bin/python

import re
import _lib


imdb = _lib.read_text_file("imdb.html")


geo = _lib.load()


for match in re.finditer(
    r"<a href=\"/title/(.*?)/.*\".*itemprop=\"name\">(.*)</a>", imdb
):
    episode_id = match.group(1)
    title = match.group(2)
    episode = _lib.get_episode_by_title(title, debug=True)
