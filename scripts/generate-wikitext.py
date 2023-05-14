#! /usr/bin/env python

from __future__ import annotations
from _lib import geo_360 as geo, Episode

"""
https://de.wikipedia.org/wiki/Vorlage:Episodenlistentabelle
https://de.wikipedia.org/wiki/Vorlage:Episodenlisteneintrag
"""


def make_ref(url: str | None) -> str:
    if not url:
        return ""
    return "<ref>" + url + "</ref>"


def generate_episode(episode: Episode, episode_no: int, absolute_no: int) -> str:
    title = episode.data["title"]
    title += make_ref(episode.fernsehserien_url)
    title += make_ref(episode.thetvdb_url)
    title += make_ref(episode.imdb_url)
    title += make_ref(episode.youtube_url)
    return (
        "{{Episodenlisteneintrag\n"
        "| NR_GES = " + str(absolute_no) + "\n"
        "| NR_ST = " + str(episode_no) + "\n"
        "| OT = " + title + "\n" + "| EA = " + episode.data["air_date"] + "\n" + "}}"
    )


def generate_season(year: int, season_no: int, episode_entries: list[str]) -> str:
    return (
        "\n=== Staffel "
        + str(season_no)
        + " ("
        + str(year)
        + ")"
        + " ===\n\n"
        + "{{Episodenlistentabelle|BREITE=100%\n"
        + "| ZUSAMMENFASSUNG = nein\n"
        + "| SORTIERBAR = nein\n"
        + "| REGISSEUR = nein\n"
        + "| DREHBUCH = nein\n"
        + "| INHALT =\n"
        + "\n".join(episode_entries)
        + "\n}}"
    )


episode_entries: list[str] = []
season_entries: list[str] = []
absolute_no = 1
episode_no = 1
year = 0
season_no = 0


def collect_episodes():
    global episode_entries
    global season_entries
    global episode_no
    if len(episode_entries) > 0:
        season_entries.append(
            generate_season(
                year=year, season_no=season_no, episode_entries=episode_entries
            )
        )
        episode_entries = []
        episode_no = 1


for episode in geo.episodes:
    if year != episode.year:
        collect_episodes()
        year: int = episode.year
        season_no += 1

    episode_entries.append(
        generate_episode(episode, episode_no=episode_no, absolute_no=absolute_no)
    )
    absolute_no += 1
    episode_no += 1

collect_episodes()


with open("360-grad-reportage.wikitext", "w") as readme:
    readme.write("\n".join(season_entries))
