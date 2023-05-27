#! /usr/bin/env python

from __future__ import annotations
from _lib import tv_show as geo, Episode
from _wiki import format_ref

"""
https://de.wikipedia.org/wiki/Vorlage:Episodenlistentabelle
https://de.wikipedia.org/wiki/Vorlage:Episodenlisteneintrag
"""


def generate_episode(episode: Episode, episode_no: int, absolute_no: int) -> str:
    title: str = episode.title
    if episode.title_fr:
        title += f" / {episode.title_fr}"
    title += format_ref(episode.fernsehserien_url)
    title += format_ref(episode.thetvdb_url)
    title += format_ref(episode.imdb_url)
    title += format_ref(episode.youtube_url)
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


def main() -> None:
    episode_entries: list[str] = []
    season_entries: list[str] = []
    absolute_no = 1
    episode_no = 1
    year = 0
    season_no = 0

    def collect_episodes() -> None:
        nonlocal episode_entries
        nonlocal season_entries
        nonlocal episode_no
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


main()
