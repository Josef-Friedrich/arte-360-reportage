#! /usr/bin/env python

import typing
import _lib

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

result = _lib.load()


def format_air_date(episode: _lib.Episode) -> str:
    if "air_date" not in episode or not episode["air_date"]:
        return ""

    return episode["air_date"]


def format_thetvdb_link(episode: _lib.Episode) -> str:
    if "thetvdb_episode_id" not in episode or "thetvdb_season_episode" not in episode:
        return ""
    base_url = result["databases"]["thetvdb"]
    id: int = episode["thetvdb_episode_id"]

    url = f"{base_url}/episodes/{id}"
    se = episode["thetvdb_season_episode"]
    return f"[{se}]({url})"


def format_fernsehserien_link(episode: _lib.Episode) -> str:
    if (
        "fernsehserien_episode_slug" not in episode
        or "fernsehserien_episode_no" not in episode
    ):
        return ""
    base_url = result["databases"]["fernsehserien"]
    slug: str = episode["fernsehserien_episode_slug"]

    url = f"{base_url}/folgen/{slug}"
    no = episode["fernsehserien_episode_no"]
    return f"[{no}]({url})"


def format_row(cells: list[typing.Any]):
    row = " | ".join(cells)
    return f"| {row} | "


rows: list[str] = []
rows.append(format_row(["air_date", "title", "thetvdb", "fernsehserien"]))
rows.append(format_row(["-", "-", "-", "-"]))
for episode in result["episodes"]:
    row: list[str] = []
    row.append(format_air_date(episode))
    row.append(episode["title"])
    row.append(format_thetvdb_link(episode))
    row.append(format_fernsehserien_link(episode))

    rows.append(format_row(row))


with open("README.md", "w") as readme:
    readme.write(str("\n".join(rows)))
