#! /usr/bin/env python

from __future__ import annotations

import argparse
import difflib
import json
import re
import typing
from datetime import date
import abc

import requests
import bs4

import termcolor
import yaml

EXPORT_FILENAME = "arte-360-reportage"


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


### yaml ######################################################################


class Yaml:
    @staticmethod
    def load(filepath: str) -> typing.Any:
        with open(filepath, "r") as y:
            return yaml.load(y, Loader=yaml.Loader)

    @staticmethod
    def save(filepath: str, data: typing.Any) -> None:
        with open(filepath, "w") as y:
            yaml.dump(
                data,
                stream=y,
                allow_unicode=True,
                sort_keys=False,
                width=72,
                indent=4,
                explicit_start=True,
            )


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


### scraper ###################################################################


class Scrapper:
    __soup: bs4.BeautifulSoup

    MARKER = "-*-*-*-"

    def __init__(self, url: str) -> None:
        page = requests.get(url)
        self.__soup = bs4.BeautifulSoup(page.content, "lxml")

    def find(self, tag: str, **kwargs: typing.Any) -> str | None:
        element = self.__soup.find(tag, **kwargs)
        if element:
            return str(element)

    def get_text(self, element: typing.Any):
        return bs4.BeautifulSoup(element, "lxml").text


class FernsehserienScrapper(Scrapper):
    @property
    def description(self) -> str | None:
        element = self.find("div", class_="episode-output-inhalt-inner")
        if element:
            text = re.sub(" *<br/?> *", self.MARKER, element)
            text = self.get_text(text)
            text = text.strip()
            text = re.sub(r"\s+", " ", text)
            text = text.replace(self.MARKER, "\n")
            return text


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
    def continent_emoji(self) -> str:
        if not self.continent:
            return ""
        if self.continent == "Afrika":
            return "⚫️"
        elif self.continent == "Amerika":
            return "🔴"
        elif self.continent == "Asien":
            # Old symbol "💚"
            return "🟡"
        elif self.continent == "Europa":
            return "⚪️"
        elif self.continent == "Ozeanien und Pole":
            return "🔵"
        return ""

    @property
    def description(self) -> str | None:
        return self.__get_str_key("description")

    @description.setter
    def description(self, description: str) -> None:
        self.data["description"] = description

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

    def export_data(self) -> EpisodeData:
        result: dict[str, typing.Any] = {}
        for key in EpisodeData.__annotations__:
            if key in self.data and self.data[key] != None:
                result[key] = self.data[key]
        return typing.cast(EpisodeData, result)


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

    def export_data(self) -> SeasonData:
        episodes: list[EpisodeData] = []
        for episode in self.episodes:
            episodes.append(episode.export_data())
        return {"no": self.no, "year": self.year, "episodes": episodes}


### main ######################################################################


class TvShowData(typing.TypedDict):
    seasons: list[SeasonData]
    databases: dict[str, str]


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
        return Yaml.load("database.yml")

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

    def export_data(self) -> TvShowData:
        data: TvShowData = self.__load()

        seasons: list[SeasonData] = []
        for season in self.seasons:
            seasons.append(season.export_data())
        data["seasons"] = seasons

        return data

    def export_to_yaml(self, filepath: str | None = None):
        if not filepath:
            filepath = EXPORT_FILENAME + ".yml"
        Yaml.save(filepath, self.export_data())

    def export_to_json(self) -> None:
        with open(EXPORT_FILENAME + ".json", "w") as j:
            json.dump(self.data, fp=j, indent=2, ensure_ascii=False)


tv_show = TvShow()


class Wiki:
    @staticmethod
    def ref(content: str | None) -> str:
        if not content or content == "":
            return ""
        return "<ref>" + content + "</ref>"

    @staticmethod
    def internetquelle(
        url: str,
        titel: str,
        abruf: str | None = None,
        website: str | None = None,
        titel_ergaenzung: str | None = None,
        herausgeber: str | None = None,
    ) -> str:
        """https://de.wikipedia.org/wiki/Vorlage:Internetquelle not usable because of
        https://de.wikipedia.org/wiki/Hilfe:Vorlagenbeschr%C3%A4nkungen"""

        def format_key_value(key: str, value: str) -> str:
            return "|" + key + "=" + value

        entries: list[str] = []

        def append(key: str, value: str) -> None:
            entries.append(format_key_value(key, value))

        append("url", url)
        append("titel", titel)

        if titel_ergaenzung:
            append("titelerg", titel_ergaenzung)

        if website:
            append("werk", website)

        if herausgeber:
            append("hrsg", herausgeber)

        if not abruf:
            abruf = date.today().isoformat()
        append("abruf", abruf)

        markup: str = " ".join(entries)
        return "{{Internetquelle " + markup + "}}"

    @staticmethod
    def titel_ergaenzung(episode: Episode) -> str:
        return f"zur Folge „{episode.title}“"

    @staticmethod
    def format_ref_imdb(episode: Episode) -> str:
        "https://developer.imdb.com/documentation/key-concepts"
        if not episode.imdb_url or not episode.imdb_episode_id:
            return ""
        return Wiki.ref(
            Wiki.internetquelle(
                url=episode.imdb_url,
                titel=f"Episoden-ID (title entity): {episode.imdb_episode_id}",
                titel_ergaenzung=Wiki.titel_ergaenzung(episode),
                herausgeber="Internet Movie Database (IMDb)",
                website="imdb.com",
            )
        )

    @staticmethod
    def format_ref_fernsehserien(episode: Episode) -> str:
        if (
            not episode.fernsehserien_episode_no
            or not episode.fernsehserien_episode_slug
            or not episode.fernsehserien_episode_id
            or not episode.fernsehserien_url
        ):
            return ""
        return Wiki.ref(
            Wiki.internetquelle(
                url=episode.fernsehserien_url,
                titel=f"Fortlaufende-Nr.: {episode.fernsehserien_episode_no}, Episoden-ID: {episode.fernsehserien_episode_id}",
                titel_ergaenzung=Wiki.titel_ergaenzung(episode),
                herausgeber="imfernsehen GmbH & Co. KG",
                website="fernsehserien.de",
            )
        )


class WikiTemplate(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def episode(episode: Episode) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def season(season: Season, episode_entries: list[str]) -> str:
        pass


class DeWiki(WikiTemplate):
    @staticmethod
    def episode(episode: Episode) -> str:
        """
        https://de.wikipedia.org/wiki/Vorlage:Episodenlisteneintrag
        """
        title: str = episode.title
        if episode.title_fr:
            title += f" / {episode.title_fr}"
        title += Wiki.ref(episode.fernsehserien_url)
        title += Wiki.ref(episode.thetvdb_url)
        title += Wiki.ref(episode.imdb_url)
        title += Wiki.ref(episode.youtube_url)
        return (
            "{{Episodenlisteneintrag\n"
            "| NR_GES = " + str(episode.overall_no) + "\n"
            "| NR_ST = " + str(episode.episode_no) + "\n"
            "| OT = " + title + "\n" + "| EA = " + episode.air_date + "\n" + "}}"
        )

    @staticmethod
    def season(season: Season, episode_entries: list[str]) -> str:
        """
        https://de.wikipedia.org/wiki/Vorlage:Episodenlistentabelle
        """
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


class FrWiki(WikiTemplate):
    @staticmethod
    def episode(episode: Episode) -> str:
        title = episode.title_fr
        if not title:
            title = "Titre inconnu"
        return (
            "|-\n"
            + f"|{episode.episode_no}\n"
            + f"|{episode.continent_emoji}\n"
            + f"| {title}"
        )

    @staticmethod
    def season(season: Season, episode_entries: list[str]) -> str:
        return (
            '\n{| class="wikitable sortable mw-collapsible mw-collapsed"\n'
            + f"|+Saison {season.no} — Année {season.year}\n"
            + '!width="8%"|N°\n'
            + '!width="5%"|\n'
            + '!width="87%"|Titre français\n'
            + "\n".join(episode_entries)
            + "\n|}"
        )


### actions ###################################################################


def scrape():
    for episode in tv_show.episodes:
        if episode.fernsehserien_url:
            scrapper = FernsehserienScrapper(episode.fernsehserien_url)
            print("\n\n" + episode.fernsehserien_url + "\n")
            description = scrapper.description
            print(description)

            if description:
                episode.description = description

        tv_show.export_to_yaml()


def generate_wikitext(language: typing.Literal["de", "fr"] = "de") -> None:
    episode_entries: list[str] = []
    season_entries: list[str] = []

    Template: WikiTemplate
    if language == "fr":
        Template = typing.cast(WikiTemplate, FrWiki)
    else:
        Template = typing.cast(WikiTemplate, DeWiki)

    for season in tv_show.seasons:
        episode_entries = []
        for episode in season.episodes:
            episode_entries.append(Template.episode(episode))
        season_entries.append(
            Template.season(season=season, episode_entries=episode_entries)
        )

    Utils.write_text_file(f"{EXPORT_FILENAME}_wiki-{language}.wikitext", season_entries)


def generate_readme():
    #     header = """
    # # 360-geo-reportage

    # https://thetvdb.com/series/272599-show

    # https://www.imdb.com/title/tt0457219

    # https://www.themoviedb.org/tv/95966-360-die-geo-reportage

    # https://www.arte.tv/de/videos/RC-014120/360-reportage/

    # https://programm.ard.de/TV/Programm/Suche?sort=date&suche=GEO+Reportage

    # https://docs.google.com/spreadsheets/d/1lL1KNkdH1Rz1BHug8OPVuFEWXzD3Ax1Q-00jBV55INg/edit?usp=sharing

    # Quelle: https://www.fernsehserien.de/arte-360grad-reportage/episodenguide
    # """

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
    parser = argparse.ArgumentParser(prog=EXPORT_FILENAME)
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-r", "--readme", action="store_true")
    parser.add_argument("-s", "--scrape", action="store_true")
    parser.add_argument("-w", "--wiki", choices=("de", "fr"))
    parser.add_argument("-y", "--yaml", action="store_true")
    return parser


def main() -> None:
    args = get_argument_parser().parse_args()

    if args.json:
        tv_show.export_to_json()

    if args.readme:
        generate_readme()

    if args.scrape:
        scrape()

    if args.wiki:
        generate_wikitext(args.wiki)

    if args.yaml:
        tv_show.export_to_yaml()


if __name__ == "__main__":
    main()
