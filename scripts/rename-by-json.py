#! /usr/bin/env python

from __future__ import annotations

import difflib
import glob
import json
import pathlib
import re
import typing

files = """
_new/Ahornsirup - Kanadas süßer Schatz (ARTE 360° Reportage) [HlFRnPw6Y04].mp4
s24/s24e22 Ahornsirup Kanadas süßer Schatz (YT HlFRnPw6Y04).mp4
"""


json_file = open("episodes.json", "r")


class Episode(typing.TypedDict):
    id: str
    season: int
    episode: int
    no: int
    title: str
    air_data: str
    duration: int
    thetvdb_episode_id: int


episodes: list[Episode] = json.load(json_file)


src_titles: list[str] = []
for episode in episodes:
    # print(episode['title'])
    src_titles.append(episode["title"])


def extract_title_from_new(rel_path: str) -> str:
    """
    _new/Sark, die Kanalinsel der Queen (360° - GEO Reportage) [ybpV9JWD6qs].mp4

    -> Sark, die Kanalinsel der Queen
    """
    rel_path = rel_path.replace("_new/", "")
    rel_path = rel_path.replace("_new/", "")
    rel_path = re.sub(r" \(.*", "", rel_path)
    return rel_path


def get_episode_by_title(title: str | None) -> Episode | None:
    if not title:
        return
    match: list[str] = difflib.get_close_matches(title, src_titles, n=1)
    if len(match) > 0:
        src_i: int = src_titles.index(match[0])
        return episodes[src_i]


dest_titles: list[str | None] = []
dest_files: list[str] = []
for rel_path in files.splitlines():
    dest_files.append(rel_path)
    if rel_path.startswith("_new"):
        title = extract_title_from_new(rel_path)
        print(title)
        dest_titles.append(title)
    else:
        dest_titles.append(None)

dest_i = 0
for title in dest_titles:
    episode: Episode | None = get_episode_by_title(title)
    if episode:
        src = pathlib.Path(dest_files[dest_i])
        print(episode["title"])
        print(src)

        season: str = str(episode["season"]).zfill(2)
        dest: str = f"s{season}/{episode['id'].lower()} {src.name}"

        dest = re.sub(r" +\(.*\) +", " ", dest)
        dest = re.sub(r"\[(.*)\]+", r"(YT \1)", dest)
        print(dest)
        # print(episode)
        # src.rename(dest)
        print()
    dest_i += 1
