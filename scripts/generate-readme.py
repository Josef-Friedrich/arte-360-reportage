#! /usr/bin/env python

import typing
import yaml

"""
# 360-geo-reportage

https://thetvdb.com/series/272599-show

https://www.imdb.com/title/tt0457219

https://www.themoviedb.org/tv/95966-360-die-geo-reportage

https://www.arte.tv/de/videos/RC-014120/360-reportage/

https://programm.ard.de/TV/Programm/Suche?sort=date&suche=GEO+Reportage

https://docs.google.com/spreadsheets/d/1lL1KNkdH1Rz1BHug8OPVuFEWXzD3Ax1Q-00jBV55INg/edit?usp=sharing

Quelle: https://www.fernsehserien.de/arte-360grad-reportage/episodenguide
"""


with open("360-grad-reportage.yml", "r") as j:
    result = yaml.load(j, Loader=yaml.Loader)


def format_air_date(episode) -> str:
    if "air_date" not in episode or not episode["air_date"]:
        return ""

    return episode["air_date"]


def format_thetvdb_link(episode) -> str:
    if "thetvdb_episode_no" not in episode or "thetvdb_season_episode" not in episode:
        return ""
    base_url = result["databases"]["thetvdb"]
    no: str = episode["thetvdb_episode_no"]

    url = f"{base_url}/episodes/{no}"
    se = episode["thetvdb_season_episode"]
    return f"[{se}]({url})"


def format_row(cells: list[typing.Any]):
    row = " | ".join(cells)
    return f"| {row} | "


rows = []
rows.append(format_row(["air_date", "title", "thetvdb"]))
rows.append(format_row(["-", "-", "-"]))
for episode in result["episodes"]:
    row = []
    row.append(format_air_date(episode))
    row.append(episode["title"])
    row.append(format_thetvdb_link(episode))

    rows.append(format_row(row))


with open("README.md", "w") as readme:
    readme.write(str("\n".join(rows)))
