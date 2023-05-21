#! /usr/bin/env python

import typing

from _lib import geo_360 as geo

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


def format_row(cells: list[typing.Any]):
    row = " | ".join(cells)
    return f"| {row} | "


rows: list[str] = []
rows.append(
    format_row(["air_date", "title", "youtube", "thetvdb", "imdb", "fernsehserien"])
)
rows.append(format_row(["-", "-", "-", "-", "-", "-"]))
for episode in geo.episodes:
    row: list[str] = []
    row.append(episode.format_air_date("%a %Y-%m-%d"))
    row.append(episode.title)
    row.append(episode.youtube_link)
    row.append(episode.thetvdb_link)
    row.append(episode.imdb_link)
    row.append(episode.fernsehserien_link)
    rows.append(format_row(row))


with open("README.md", "w") as readme:
    readme.write(str("\n".join(rows)))
