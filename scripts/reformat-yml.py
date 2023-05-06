#! /usr/bin/env python

import typing
import yaml


with open("360-grad-reportage.yml", "r") as j:
    result = yaml.load(j, Loader=yaml.Loader)


new: list[dict[str, typing.Any]] = []
for old in result["episodes"]:
    print(old)
    episode = {
        "title": old["title"],
        "air_date": old["air_date"],
    }
    if "duration" in old and old["duration"]:
        episode["duration"] = old["duration"]

    if "id" in old:
        episode["thetvdb_season_episode"] = old["id"]

    if "thetvdb_episode_no" in old:
        episode["thetvdb_episode_no"] = old["thetvdb_episode_no"]
    new.append(episode)

result["episodes"] = new

with open("360-grad-reportage_new.yml", "w") as y:
    yaml.dump(result, stream=y, allow_unicode=True, sort_keys=False)
