#! /usr/bin/env python

from __future__ import annotations
from _tvshow import tv_show, Episode
from _wiki import format_ref
from _season import Season

"""
https://de.wikipedia.org/wiki/Vorlage:Episodenlistentabelle
https://de.wikipedia.org/wiki/Vorlage:Episodenlisteneintrag
"""


def generate_episode(episode: Episode) -> str:
    title: str = episode.title
    if episode.title_fr:
        title += f" / {episode.title_fr}"
    title += format_ref(episode.fernsehserien_url)
    title += format_ref(episode.thetvdb_url)
    title += format_ref(episode.imdb_url)
    title += format_ref(episode.youtube_url)
    return (
        "{{Episodenlisteneintrag\n"
        "| NR_GES = " + str(episode.overall_no) + "\n"
        "| NR_ST = " + str(episode.episode_no) + "\n"
        "| OT = " + title + "\n" + "| EA = " + episode.air_date + "\n" + "}}"
    )


def generate_season(season: Season, episode_entries: list[str]) -> str:
    return (
        "\n=== Staffel "
        + str(season.no)
        + " ("
        + str(season.year)
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

    for season in tv_show.seasons:
        episode_entries = []
        for episode in season.episodes:
            episode_entries.append(generate_episode(episode))
        season_entries.append(
            generate_season(season=season, episode_entries=episode_entries)
        )

    with open("360-grad-reportage.wikitext", "w") as readme:
        readme.write("\n".join(season_entries))


main()
