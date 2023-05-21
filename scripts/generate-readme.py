#! /usr/bin/env python

from __future__ import annotations

import typing

from _lib import tv_show
from _episode import Episode

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


def _format_title(episode: Episode) -> str:
    title: str = episode.title
    if episode.title_fr:
        title += f"<br>fr: *{episode.title_fr}*"
    if episode.title_en:
        title += f"<br>en: *{episode.title_en}*"
    return title


def _format_row(cells: list[typing.Any]) -> str:
    row: str = " | ".join(cells)
    return f"| {row} | "


def _format_table(header: list[str], rows: list[list[str]]) -> str:
    rendered_rows: list[str] = []
    rendered_rows.append(_format_row(header))

    separator: list[str] = []
    for _ in header:
        separator.append("---")
    rendered_rows.append(_format_row(separator))

    for row in rows:
        rendered_rows.append(_format_row(row))
    return "\n".join(rendered_rows)


def _assemble_row(episode: Episode) -> list[str]:
    row: list[str] = []
    row.append(episode.format_air_date("%a %Y-%m-%d"))
    row.append(_format_title(episode))
    row.append(episode.youtube_link)
    row.append(episode.thetvdb_link)
    row.append(episode.imdb_link)
    row.append(episode.fernsehserien_link)
    return row


def main() -> None:
    rows: list[list[str]] = []

    for episode in tv_show.episodes:
        rows.append(_assemble_row(episode))

    with open("README.md", "w") as readme:
        readme.write(
            _format_table(
                ["air_date", "title", "youtube", "thetvdb", "imdb", "fernsehserien"],
                rows,
            )
        )


main()
