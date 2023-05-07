import difflib
import json
import typing

import termcolor
import typing_extensions
import yaml


class Episode(typing.TypedDict):
    title: str
    alias: str
    title_fr: str
    title_en: str
    air_date: str
    duration: int
    thetvdb_season_episode: str
    thetvdb_episode_id: int
    fernsehserien_air_date: str
    fernsehserien_episode_no: int
    fernsehserien_episode_slug: str
    fernsehserien_episode_id: int
    imdb_episode_id: str
    index: typing_extensions.NotRequired[int]


class GeoMetaData(typing.TypedDict):
    episodes: list[Episode]
    databases: dict[str, str]


YAML_FILENAME = "360-grad-reportage.yml"


def read_text_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def normalize_title(title: str) -> str:
    title = title.replace(", ", " ")
    title = title.replace(": ", " ")
    title = title.replace(" - ", " ")
    return title.lower()


class Geo360:
    data: GeoMetaData

    titles: dict[str, int]

    def __init__(self) -> None:
        self.data = self.__load()
        self.__add_indexes()

        self.titles = {}
        for episode in self.data["episodes"]:
            if "index" in episode:
                self.titles[episode["title"]] = episode["index"]
                if "alias" in episode:
                    self.titles[episode["alias"]] = episode["index"]
                if "title_fr" in episode:
                    self.titles[episode["title_fr"]] = episode["index"]
                if "title_en" in episode:
                    self.titles[episode["title_en"]] = episode["index"]

    def __load(self) -> GeoMetaData:
        with open(YAML_FILENAME, "r") as y:
            result: GeoMetaData = yaml.load(y, Loader=yaml.Loader)
            return result

    def get_episode_by_title(
        self, title: str | None, debug: bool = False
    ) -> Episode | None:
        if not title:
            return
        found: list[str] = difflib.get_close_matches(title, self.titles.keys(), n=1)
        episode = None
        if len(found) > 0:
            episode = self.data["episodes"][self.titles[found[0]]]

        if debug:
            if not episode:
                print(f"No match found for: {termcolor.colored(title, color='red')}")
            elif normalize_title(title) != normalize_title(episode["title"]):
                print(
                    f"{termcolor.colored(title, color='yellow')} <> {termcolor.colored(episode['title'], color='blue')}"
                )

        return episode

    @property
    def episodes(self) -> list[Episode]:
        self.__add_indexes()
        return self.data["episodes"]

    def __add_indexes(self) -> None:
        i: int = 0
        for episode in self.data["episodes"]:
            episode["index"] = i
            i += 1

    def __remove_indexes(self) -> None:
        for episode in self.data["episodes"]:
            del episode["index"]

    def reformat(self) -> None:
        for old in self.episodes:
            episode: dict[str, str | int] = {
                "title": old["title"],
                "air_date": old["air_date"],
            }
            if "duration" in old and old["duration"]:
                episode["duration"] = old["duration"]

    def export_to_json(self) -> None:
        self.__remove_indexes()
        with open("360-grad-reportage.json", "w") as j:
            json.dump(self.data, fp=j, indent=2, ensure_ascii=False)

    def __write(self) -> None:
        with open(YAML_FILENAME, "w") as y:
            yaml.dump(self.data, stream=y, allow_unicode=True, sort_keys=False)

    def save(self) -> None:
        self.__remove_indexes()
        self.__write()


geo_360 = Geo360()
