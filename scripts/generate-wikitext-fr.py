#! /usr/bin/env python

from __future__ import annotations

from typing import TYPE_CHECKING

from _tvshow import Episode, tv_show

if TYPE_CHECKING:
    from _season import Season


def generate_episode(episode: Episode) -> str:
    title = episode.title_fr
    if not title:
        title = "Titre inconnu"
    return "|-\n" + f"|{episode.episode_no}\n" + "|🔵\n" + f"| {title}"


def generate_season(season: Season, episode_entries: list[str]) -> str:
    return (
        '\n{| class="wikitable sortable mw-collapsible mw-collapsed"\n'
        + f"|+Saison {season.no} — Année {season.year}\n"
        + '!width="8%"|N°\n'
        + '!width="5%"|\n'
        + '!width="87%"|Titre français\n'
        + "\n".join(episode_entries)
        + "\n|}"
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

    with open("360-grad-reportage_fr.wikitext", "w") as readme:
        readme.write("\n".join(season_entries))


main()
