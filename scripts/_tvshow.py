from __future__ import annotations

import difflib
import json
import typing
from typing import TYPE_CHECKING

import termcolor
import yaml
from _episode import Episode
from _lib import normalize_title
from _season import Season

if TYPE_CHECKING:
    from _season import Season, SeasonData


class TvShowData(typing.TypedDict):
    seasons: list[SeasonData]
    databases: dict[str, str]


YAML_FILENAME = "360-grad-reportage.yml"


class TvShow:
    data: TvShowData

    titles: dict[str, int]

    episodes: list[Episode]

    seasons: list[Season]

    def __init__(self) -> None:
        self.data = self.__load()
        self.__generate_season_episodes()
        self.titles = self.__generate_title_list()

    def __load(self) -> TvShowData:
        with open(YAML_FILENAME, "r") as y:
            result: TvShowData = yaml.load(y, Loader=yaml.Loader)
            return result

    def __generate_season_episodes(self) -> None:
        self.episodes: list[Episode] = []
        self.seasons: list[Season] = []
        overall_no: int = 1
        for season_data in self.data["seasons"]:
            episodes: list[Episode] = []
            episode_no: int = 1
            for episode_data in season_data["episodes"]:
                episode = Episode(
                    episode_data,
                    tv_show=self.data,
                    overall_no=overall_no,
                    season_no=season_data["no"],
                    episode_no=episode_no,
                )
                self.episodes.append(episode)
                episodes.append(episode)
                overall_no += 1
                episode_no += 1
            self.seasons.append(Season(season_data, episodes))

    def __generate_title_list(self) -> dict[str, int]:
        titles: dict[str, int] = {}
        for episode in self.episodes:
            index: int = episode.overall_no - 1
            titles[episode.title] = index
            if episode.alias:
                titles[episode.alias] = index
            if episode.title_fr:
                titles[episode.title_fr] = index
            if episode.title_en:
                titles[episode.title_en] = index
        return titles

    def get_episode_by_title(
        self, title: str | None, debug: bool = False
    ) -> Episode | None:
        if not title:
            return
        found: list[str] = difflib.get_close_matches(title, self.titles.keys(), n=1)
        episode = None
        if len(found) > 0:
            episode = self.episodes[self.titles[found[0]]]

        if debug:
            if not episode:
                print(f"No match found for: {termcolor.colored(title, color='red')}")
            elif normalize_title(title) != normalize_title(episode.title):
                print(
                    f"{termcolor.colored(title, color='yellow')} <> {termcolor.colored(episode.title, color='blue')}"
                )

        return episode

    # @property
    # def episodes_data(self) -> list[EpisodeData]:
    #     self.__add_indexes()
    #     return self.data["episodes"]

    # def reformat(self) -> None:
    #     for old in self.episodes_data:
    #         episode: dict[str, str | int] = {
    #             "title": old["title"],
    #             "air_date": old["air_date"],
    #         }
    #         if "duration" in old and old["duration"]:
    #             episode["duration"] = old["duration"]

    def export_to_json(self) -> None:
        with open("360-grad-reportage.json", "w") as j:
            json.dump(self.data, fp=j, indent=2, ensure_ascii=False)

    def __write(self) -> None:
        with open(YAML_FILENAME, "w") as y:
            yaml.dump(self.data, stream=y, allow_unicode=True, sort_keys=False)

    def save(self) -> None:
        self.__write()


tv_show = TvShow()
