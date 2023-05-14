import difflib
import json
import typing
import re

import termcolor
import typing_extensions
import yaml


class EpisodeData(typing.TypedDict):
    title: str
    alias: str
    title_fr: str
    title_en: str
    air_date: str
    duration: int
    season: int
    episode: int
    thetvdb_season_episode: str
    thetvdb_episode_id: int
    fernsehserien_air_date: str
    fernsehserien_episode_no: int
    fernsehserien_episode_slug: str
    fernsehserien_episode_id: int
    imdb_episode_id: str
    youtube_video_id: str
    index: typing_extensions.NotRequired[int]


class TvShowData(typing.TypedDict):
    episodes: list[EpisodeData]
    databases: dict[str, str]


class Episode:
    data: EpisodeData
    tv_show: TvShowData

    def __init__(self, data: EpisodeData, tv_show: TvShowData) -> None:
        self.data = data
        self.tv_show = tv_show

    @property
    def title(self) -> str:
        return self.data["title"]

    @property
    def air_date(self) -> str:
        if "air_date" not in self.data or not self.data["air_date"]:
            return ""
        return self.data["air_date"]

    def __make_markdown_link(
        self, title: str | typing.Any | None, url: str | None
    ) -> str:
        if not title or not url:
            return ""
        return f"[{str(title)}]({url})"

    @property
    def thetvdb_url(self) -> str | None:
        if (
            "thetvdb_episode_id" not in self.data
            or "thetvdb_season_episode" not in self.data
        ):
            return
        base_url: str = self.tv_show["databases"]["thetvdb"]
        id: int = self.data["thetvdb_episode_id"]
        return f"{base_url}/episodes/{id}"

    @property
    def thetvdb_link(self) -> str:
        if "thetvdb_season_episode" not in self.data:
            return ""
        return self.__make_markdown_link(
            self.data["thetvdb_season_episode"], self.thetvdb_url
        )

    @property
    def imdb_url(self) -> str | None:
        if "imdb_episode_id" not in self.data:
            return
        episode_id: str = self.data["imdb_episode_id"]
        return f"https://www.imdb.com/title/{episode_id}"

    @property
    def imdb_link(self) -> str:
        if "imdb_episode_id" not in self.data:
            return ""
        return self.__make_markdown_link(self.data["imdb_episode_id"], self.imdb_url)

    @property
    def fernsehserien_url(self) -> str | None:
        if (
            "fernsehserien_episode_slug" not in self.data
            or "fernsehserien_episode_no" not in self.data
        ):
            return
        base_url: str = self.tv_show["databases"]["fernsehserien"]
        slug: str = self.data["fernsehserien_episode_slug"]
        return f"{base_url}/folgen/{slug}"

    @property
    def fernsehserien_link(self) -> str:
        if "fernsehserien_episode_no" not in self.data:
            return ""
        return self.__make_markdown_link(
            self.data["fernsehserien_episode_no"], self.fernsehserien_url
        )

    @property
    def youtube_url(self) -> str | None:
        if "youtube_video_id" not in self.data:
            return
        video_id: str = self.data["youtube_video_id"]
        return f"https://www.youtube.com/watch?v={video_id}"

    @property
    def youtube_link(self) -> str:
        if "youtube_video_id" not in self.data:
            return ""
        return self.__make_markdown_link(
            self.data["youtube_video_id"], self.youtube_url
        )

    def __get_season_or_episode(self, episode: bool = True) -> int | None:
        if not "thetvdb_season_episode" in self.data:
            return

        if episode:
            regex = r"s\d+e(\d+)"
        else:
            regex = r"s(\d)+e\d+"
        match = re.match(regex, self.data["thetvdb_season_episode"], re.IGNORECASE)
        if match:
            return int(match.group(1))

    @property
    def season_no(self):
        return self.__get_season_or_episode(False)

    @property
    def episode_no(self):
        return self.__get_season_or_episode(True)

    @property
    def year(self) -> int:
        return int(self.data["air_date"][0:4])


YAML_FILENAME = "360-grad-reportage.yml"


def read_text_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def clean_title(title: str) -> str:
    title = title.replace("–", "-")
    title = re.sub(r" *\(.+\) *", " ", title)
    title = title.strip()
    title = re.sub(r"  +", " ", title)
    title = re.sub(r"GEO Reportage *[:-] +", "", title)
    title = re.sub(r"^\d+ *- *", "", title)
    return title


def normalize_title(title: str) -> str:
    title = title.replace(", ", " ")
    title = title.replace(": ", " ")
    title = title.replace(" - ", " ")
    return title.lower()


class TvShow:
    data: TvShowData

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

    def __load(self) -> TvShowData:
        with open(YAML_FILENAME, "r") as y:
            result: TvShowData = yaml.load(y, Loader=yaml.Loader)
            return result

    def get_episode_by_title(
        self, title: str | None, debug: bool = False
    ) -> EpisodeData | None:
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
    def episodes_data(self) -> list[EpisodeData]:
        self.__add_indexes()
        return self.data["episodes"]

    @property
    def episodes(self) -> list[Episode]:
        self.__add_indexes()
        result: list[Episode] = []
        for episode_data in self.episodes_data:
            result.append(Episode(episode_data, self.data))
        return result

    def __add_indexes(self) -> None:
        i: int = 0
        for episode in self.data["episodes"]:
            episode["index"] = i
            i += 1

    def __remove_indexes(self) -> None:
        for episode in self.data["episodes"]:
            del episode["index"]

    def reformat(self) -> None:
        for old in self.episodes_data:
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


geo_360 = TvShow()
