#! /usr/bin/env python

import csv
import json
from typing import Any
import re


def extract_season_episode(season_episode: str, episode: bool = False) -> str:
    match = re.match(r"S([0-9]+)E([0-9]+)", season_episode)
    if match:
        if episode:
            return match[2]
        return match[1]

    raise Exception(season_episode)


def extract_duration(duration: str) -> int | None:
    if duration != "":
        return int(duration)


with open("episodes.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')

    episodes: list[dict[str, Any]] = []
    for episode in reader:
        if episode[0] == "season/episode":
            continue

        e: dict[str, str | int | None] = {}
        e["season"] = int(extract_season_episode(episode[0]))
        e["episode"] = int(extract_season_episode(episode[0], True))
        e["season_episode_id"] = episode[0]
        e["no"] = int(episode[1])
        e["title"] = episode[2]
        e["air_date"] = episode[3]
        e["duration"] = extract_duration(episode[4])
        e["thetvdb_episode_no"] = int(episode[6])
        episodes.append(e)

json_dump: str = json.dumps(episodes, indent=2, ensure_ascii=False)

with open("episodes.json", "w") as json_file:
    json_file.write(json_dump)
