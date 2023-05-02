#! /usr/bin/env python

import csv
import json
from typing import Any
import re

def extract_season_episode(season_episode: str)-> str:
    match = re.match(r"S([0-9])+E[0-9]+", season_episode)
    if match:
        return match[1]

    raise Exception(season_episode)

with open('episodes.csv', newline='') as csvfile:

    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    episodes: list[dict[str, Any]] = []
    for episode in reader:
        if episode[0] == 'season/episode':
            continue

        j: dict[str, str] = {}
        j['season'] = extract_season_episode(episode[0]),
        j['episode'] = str(episode[0]),
        j['no'] = episode[1]
        j['title'] = episode[2]
        episodes.append(j)

print(json.dumps(episodes, indent=2))
