#! /usr/bin/env python

from __future__ import annotations

import argparse
import difflib
import json
import re
import typing
from datetime import date

import termcolor
import yaml

### utils #####################################################################


class Utils:
    @staticmethod
    def read_text_file(file_path: str) -> str:
        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def write_text_file(file_path: str, content: str | list[str]) -> None:
        if isinstance(content, list):
            content = "\n".join(content)
        with open(file_path, "w") as readme:
            readme.write(content)

    @staticmethod
    def clean_title(title: str) -> str:
        title = title.replace("–", "-")
        title = re.sub(r" *\(.+\) *", " ", title)
        title = title.strip()
        title = re.sub(r"  +", " ", title)
        title = re.sub(r"GEO Reportage *[:-] +", "", title)
        title = re.sub(r"^\d+ *- *", "", title)
        return title

    @staticmethod
    def normalize_title(title: str) -> str:
        title = title.replace(", ", " ")
        title = title.replace(": ", " ")
        title = title.replace(" - ", " ")
        return title.lower()


### dvd #######################################################################


class DvdData(typing.TypedDict):
    title: str
    """for example ``KOLUMBIEN - Die rasenden Engel der Linea 5``"""

    dvd_count: int
    """for example ``1``"""

    ean: str
    """for example ``4009496401519``"""

    release_date: str
    """for example ``2007-01-01``"""

    production_date: str
    """for example ``2007-01-01``"""

    duration: int
    """for example ``52``"""

    mediamops: str
    """for example ``M0B09SDJQGBH``"""

    asin: str
    """for example ```B09SDJQGBH`"""

    episodes: list[str]


### episode ###################################################################


class EpisodeData(typing.TypedDict):
    overall_no: int
    """for example ``613``"""

    season_no: int
    """for example ``3``"""

    episode_no: int
    """for example ``4``"""

    title: str
    """German title"""

    title_fr: str
    """French title"""

    title_en: str
    """English title"""

    alias: str
    """Different German title"""

    topic: str
    """For example ``Traum-Städte``"""

    continent: typing.Literal[
        "Europa", "Amerika", "Asien", "Afrika", "Ozeanien und Pole"
    ]

    description: str
    """Longest description that can be found"""

    description_short: str
    """two sentences generate by openai"""

    air_date: str
    """for example ``2020-08-16``"""

    duration: int
    """for example ``52``"""

    fernsehserien_air_date: str
    """for example ``2020-08-09``"""

    fernsehserien_episode_no: int
    """for example ``117``"""

    fernsehserien_episode_slug: str
    """for example ``117-die-bernsteintaucher-339440``"""

    fernsehserien_episode_id: int
    """for example ``339440``"""

    imdb_episode_id: str
    """for example ``tt21801660``"""

    thetvdb_season_episode: str
    """for example ``S22E14``"""

    thetvdb_episode_id: int
    """for example ``7933483``"""

    youtube_video_id: str
    """for example ``wriortwg56E``"""


class Episode:
    data: EpisodeData
    tv_show: TvShowData

    overall_no: int
    season_no: int
    episode_no: int

    def __init__(
        self,
        data: EpisodeData,
        tv_show: TvShowData,
        overall_no: int,
        season_no: int,
        episode_no: int,
    ) -> None:
        self.data = data
        self.tv_show = tv_show
        self.overall_no = overall_no
        self.season_no = season_no
        self.episode_no = episode_no

    @property
    def title(self) -> str:
        return self.data["title"]

    def __get_str_key(self, key: str) -> str | None:
        if key in self.data and self.data[key] != "":
            return typing.cast(str, self.data[key])

    @property
    def title_fr(self) -> str | None:
        return self.__get_str_key("title_fr")

    @property
    def title_en(self) -> str | None:
        return self.__get_str_key("title_en")

    @property
    def alias(self) -> str | None:
        return self.__get_str_key("alias")

    @property
    def continent(self) -> str | None:
        return self.__get_str_key("continent")

    @property
    def air_date(self) -> str:
        if "air_date" not in self.data or not self.data["air_date"]:
            return ""
        return self.data["air_date"]

    @property
    def air_date_date(self) -> None | date:
        if "air_date" in self.data and self.data["air_date"]:
            return date.fromisoformat(self.data["air_date"])

    def format_air_date(self, format: str) -> str:
        d = self.air_date_date
        if not d:
            return ""
        return d.strftime(format)

    def __make_markdown_link(
        self, title: str | typing.Any | None, url: str | None
    ) -> str:
        if not title or not url:
            return ""
        return f"[{str(title)}]({url})"

    @property
    def thetvdb_season_episode(self) -> str | None:
        if "thetvdb_season_episode" not in self.data:
            return
        return self.data["thetvdb_season_episode"]

    @property
    def thetvdb_episode_id(self) -> int | None:
        if "thetvdb_episode_id" not in self.data:
            return
        return self.data["thetvdb_episode_id"]

    @property
    def thetvdb_url(self) -> str | None:
        if not self.thetvdb_episode_id:
            return
        base_url: str = self.tv_show["databases"]["thetvdb"]
        id: int = self.thetvdb_episode_id
        return f"{base_url}/episodes/{id}"

    @property
    def thetvdb_link(self) -> str:
        if "thetvdb_season_episode" not in self.data:
            return ""
        return self.__make_markdown_link(
            self.data["thetvdb_season_episode"], self.thetvdb_url
        )

    @property
    def imdb_episode_id(self) -> str | None:
        "For example: ``tt10007904``"
        if "imdb_episode_id" in self.data:
            return self.data["imdb_episode_id"]

    @property
    def imdb_url(self) -> str | None:
        if not self.imdb_episode_id:
            return
        return f"https://www.imdb.com/title/{self.imdb_episode_id}"

    @property
    def imdb_link(self) -> str:
        if "imdb_episode_id" not in self.data:
            return ""
        return self.__make_markdown_link(self.data["imdb_episode_id"], self.imdb_url)

    @property
    def fernsehserien_episode_no(self) -> int | None:
        if "fernsehserien_episode_no" in self.data:
            return self.data["fernsehserien_episode_no"]

    @property
    def fernsehserien_episode_id(self) -> int | None:
        if "fernsehserien_episode_id" in self.data:
            return self.data["fernsehserien_episode_id"]

    @property
    def fernsehserien_episode_slug(self) -> str | None:
        if "fernsehserien_episode_slug" in self.data:
            return self.data["fernsehserien_episode_slug"]

    @property
    def fernsehserien_url(self) -> str | None:
        if not self.fernsehserien_episode_slug:
            return
        base_url: str = self.tv_show["databases"]["fernsehserien"]
        slug: str = self.fernsehserien_episode_slug
        return f"{base_url}/folgen/{slug}"

    @property
    def fernsehserien_link(self) -> str:
        if not self.fernsehserien_episode_no:
            return ""
        return self.__make_markdown_link(
            self.fernsehserien_episode_no, self.fernsehserien_url
        )

    @property
    def youtube_video_id(self) -> str | None:
        if "youtube_video_id" not in self.data:
            return
        return self.data["youtube_video_id"]

    @property
    def youtube_url(self) -> str | None:
        if not self.youtube_video_id:
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

    # def __get_season_or_episode(self, episode: bool = True) -> int | None:
    #     if not "thetvdb_season_episode" in self.data:
    #         return

    #     if episode:
    #         regex = r"s\d+e(\d+)"
    #     else:
    #         regex = r"s(\d)+e\d+"
    #     match = re.match(regex, self.data["thetvdb_season_episode"], re.IGNORECASE)
    #     if match:
    #         return int(match.group(1))

    @property
    def year(self) -> int:
        return int(self.data["air_date"][0:4])


### season ####################################################################


class SeasonData(typing.TypedDict):
    no: int
    year: int
    episodes: list[EpisodeData]


class Season:
    data: SeasonData

    episodes: list[Episode]

    def __init__(self, data: SeasonData, episodes: list[Episode]) -> None:
        self.data: SeasonData = data
        self.episodes = episodes

    @property
    def no(self) -> int:
        return self.data["no"]

    @property
    def year(self) -> int:
        return self.data["year"]


### main ######################################################################


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
            elif Utils.normalize_title(title) != Utils.normalize_title(episode.title):
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


### markdown ##################################################################


class Markdown:
    @staticmethod
    def table(header: list[str], rows: list[list[str]]) -> str:
        def _format_row(cells: list[typing.Any]) -> str:
            row: str = " | ".join(cells)
            return f"| {row} | "

        rendered_rows: list[str] = []
        rendered_rows.append(_format_row(header))

        separator: list[str] = []
        for _ in header:
            separator.append("---")
        rendered_rows.append(_format_row(separator))

        for row in rows:
            rendered_rows.append(_format_row(row))
        return "\n".join(rendered_rows)


### actions ###################################################################


def generate_readme():
    def _format_title(episode: Episode) -> str:
        title: str = episode.title
        if episode.title_fr:
            title += f"<br>fr: *{episode.title_fr}*"
        if episode.title_en:
            title += f"<br>en: *{episode.title_en}*"
        return title

    def _format_links(episode: Episode) -> str:
        links: list[str] = []

        def prefix_caption(caption: str, link: str) -> str:
            return f"{caption}: {link}"

        def append(caption: str, link: str | None) -> None:
            if link and link != "":
                links.append(prefix_caption(caption, link))

        if episode.youtube_video_id:
            append("youtube", episode.youtube_link)

        if episode.thetvdb_season_episode:
            append("thetvdb", episode.thetvdb_link)

        if episode.imdb_episode_id:
            append("imdb", episode.imdb_link)

        if episode.fernsehserien_episode_no:
            append("fernsehserien", episode.fernsehserien_link)

        return "<br>".join(links)

    def _assemble_row(episode: Episode) -> list[str]:
        row: list[str] = []
        row.append(episode.format_air_date("%a %Y-%m-%d"))
        row.append(_format_title(episode))
        row.append(_format_links(episode))

        return row

    rows: list[list[str]] = []

    for episode in tv_show.episodes:
        rows.append(_assemble_row(episode))

    Utils.write_text_file(
        "README.md",
        Markdown.table(
            ["air_date", "title", "links"],
            rows,
        ),
    )


### main ######################################################################


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arte-360-reportage-script")
    parser.add_argument("-r", "--readme", action="store_true")
    parser.add_argument("-j", "--json", action="store_true")

    return parser


def main() -> None:
    args = get_argument_parser().parse_args()

    if args.json:
        tv_show.export_to_json()

    if args.readme:
        generate_readme()

if __name__ == "__main__":
    main()
