#! /usr/bin/env python

from __future__ import annotations

import abc
import argparse
import difflib
import json
import pathlib
import re
import typing
from datetime import date

import bs4
import googleapiclient
import requests
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
        with open(filepath, mode="r") as y:
            return yaml.load(y, Loader=yaml.Loader)

    @staticmethod
    def save(filepath: str, data: typing.Any) -> None:
        with open(filepath, mode="w") as y:
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
    def link(title: str | typing.Any | None, url: str | None) -> str:
        if not title or not url:
            return ""
        return f"[{str(title)}]({url})"

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


class YouTube:
    YOUTUBE_API_SERVICE_NAME = "youtube"

    YOUTUBE_API_VERSION = "v3"

    resource: typing.Any

    def __init__(self):
        key = self.__load_key()
        self.resource = self.get_youtube_resource(key)

    def __load_key(self) -> str:
        keys = json.load(open(pathlib.Path.home() / ".youtube-api.json", mode="r"))
        return keys["api_key"]

    def get_youtube_resource(self, key: str) -> typing.Any:
        return googleapiclient.discovery.build(  # type: ignore
            self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=key
        )

    def fetch_videos_by_playlist(self, playlist_id: str):
        result = (
            self.resource.playlistItems()
            .list(part="snippet", playlistId=playlist_id, maxResults=50)
            .execute()
        )

        next_page_token = result.get("nextPageToken")  # type: ignore
        while "nextPageToken" in result:
            if not next_page_token:
                continue
            next_page = (
                self.resource.playlistItems()
                .list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token,
                )
                .execute()
            )
            if "items" in result and "items" in next_page:
                result["items"] = result["items"] + next_page["items"]

            if "nextPageToken" not in next_page:
                result.pop("nextPageToken", None)
            else:
                next_page_token: str = next_page["nextPageToken"]

        return result

    def get_playlist_id_of_channel(self, channel_id: str) -> str | None:
        result = (
            self.resource.channels()
            .list(part="contentDetails", id=channel_id)
            .execute()
        )

        if "items" in result:
            if len(result["items"]) > 0:
                channel = result["items"][0]
                if "contentDetails" in channel:
                    content_details = channel["contentDetails"]
                    if "relatedPlaylists" in content_details:
                        related_playlists = content_details["relatedPlaylists"]
                        if "uploads" in related_playlists:
                            return related_playlists["uploads"]

    def fetch_videos_by_channel(self, channel_id: str):
        playlist_id = self.get_playlist_id_of_channel(channel_id)
        if not playlist_id:
            raise Exception(f"No upload playlist found for channel {channel_id}")
        return self.fetch_videos_by_playlist(playlist_id)


class Scrapper:
    __soup: bs4.BeautifulSoup

    MARKER = "-*-*-*-"

    def __init__(self, url: str) -> None:
        page = requests.get(url)
        self.__soup = bs4.BeautifulSoup(page.content, "lxml")

    def find(self, tag_name: str, **kwargs: typing.Any) -> bs4.Tag | None:
        tag = self.__soup.find(tag_name, **kwargs)
        if tag and isinstance(tag, bs4.Tag):
            return tag

    def find_str(self, tag_name: str, **kwargs: typing.Any) -> str | None:
        tag = self.find(tag_name, **kwargs)
        if tag:
            return str(tag)

    def get_text(self, element: typing.Any):
        return bs4.BeautifulSoup(element, "lxml").text


class FernsehserienScrapper(Scrapper):
    @property
    def description(self) -> str | None:
        element = self.find_str("div", class_="episode-output-inhalt-inner")
        if element:
            text = re.sub(" *<br/?> *", self.MARKER, element)
            text = self.get_text(text)
            text = text.strip()
            text = re.sub(r"\s+", " ", text)
            text = text.replace(self.MARKER, "\n")
            return text

    @property
    def director(self) -> str | None:
        li = self.find("li", itemprop="director")
        if li:
            dt = li.find("dt", itemprop="name")
            if dt:
                return dt.text


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

    director: str
    """Regie"""

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

    def __get_str_key(self, key: str) -> str | None:
        if key in self.data and self.data[key] != "":
            return typing.cast(str, self.data[key])

    def __get_int_key_safe(self, key: str) -> int:
        if key in self.data and self.data[key] != "":
            return typing.cast(int, self.data[key])
        else:
            raise Exception("int not found")

    @property
    def overall_no(self) -> int:
        return self.__get_int_key_safe("overall_no")

    @overall_no.setter
    def overall_no(self, no: int) -> None:
        self.data["overall_no"] = no

    @property
    def season_no(self) -> int:
        return self.__get_int_key_safe("season_no")

    @season_no.setter
    def season_no(self, no: int) -> None:
        self.data["season_no"] = no

    @property
    def episode_no(self) -> int:
        return self.__get_int_key_safe("episode_no")

    @episode_no.setter
    def episode_no(self, no: int) -> None:
        self.data["episode_no"] = no

    @property
    def title(self) -> str:
        return self.data["title"]

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
    def description_short(self) -> str | None:
        return self.__get_str_key("description_short")

    @property
    def director(self) -> str | None:
        return self.__get_str_key("director")

    @director.setter
    def director(self, director: str) -> None:
        self.data["director"] = director

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
    def link(title: str | typing.Any | None, url: str | None) -> str:
        """https://de.wikipedia.org/wiki/Hilfe:Links#Links_zu_externen_Webseiten_(Weblinks,_URLs)"""
        if not title or not url:
            return ""
        return f"[{url} {title}]"

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
    def ref_imdb(episode: Episode) -> str:
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
    def ref_fernsehserien(episode: Episode) -> str:
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
    def ref(episode: Episode) -> str:
        def link_fernsehserien(episode: Episode) -> str:
            if not episode.fernsehserien_episode_no:
                return ""
            return (
                "Folge "
                + Wiki.link(episode.fernsehserien_episode_no, episode.fernsehserien_url)
                + " Folgen-ID "
                + Wiki.link(episode.fernsehserien_episode_id, episode.fernsehserien_url)
            )

        def link_youtube(episode: Episode) -> str:
            if not episode.youtube_video_id:
                return ""
            return "Video-ID " + Wiki.link(
                episode.youtube_video_id, episode.youtube_url
            )

        def link_imdb(episode: Episode) -> str:
            if not episode.imdb_episode_id:
                return ""
            return "Titel-ID " + Wiki.link(episode.imdb_episode_id, episode.imdb_url)

        def link_thetvdb(episode: Episode) -> str:
            if not episode.thetvdb_season_episode:
                return ""
            return (
                "Staffel/Episode "
                + Wiki.link(episode.thetvdb_season_episode, episode.thetvdb_url)
                + " Episoden-ID "
                + Wiki.link(episode.thetvdb_episode_id, episode.thetvdb_url)
            )

        links: list[str] = []

        def prefix_caption(caption: str, link: str) -> str:
            return f"''{caption}'': {link}"

        def append(caption: str, link: str | None) -> None:
            if link and link != "":
                links.append(prefix_caption(caption, link))

        if episode.fernsehserien_episode_no:
            append("fernsehserien.de", link_fernsehserien(episode))

        if episode.thetvdb_season_episode:
            append("thetvdb.com", link_thetvdb(episode))

        if episode.imdb_episode_id:
            append("imdb.com", link_imdb(episode))

        if episode.youtube_video_id:
            append("youtube.com", link_youtube(episode))

        return Wiki.ref(
            f"Internetquellen zur Episode ''„{episode.title}“'': " + ", ".join(links)
        )

    @staticmethod
    def key(key: str, value: typing.Any) -> str:
        return f"| {key} = {value}\n"

    @staticmethod
    def episode(episode: Episode) -> str:
        """
        https://de.wikipedia.org/wiki/Vorlage:Episodenlisteneintrag

        https://de.wikipedia.org/wiki/Vorlage:Episodenlisteneintrag2
        """
        key = DeWiki.key

        title: str = episode.title + DeWiki.ref(episode)

        template = "Episodenlisteneintrag"
        summary = ""
        if episode.description_short:
            template = "Episodenlisteneintrag2"
            summary = key("ZF", episode.description_short)

        title_fr = episode.title_fr
        if not title_fr:
            title_fr = "-"

        director = episode.director
        if not director:
            director = "-"

        return (
            "{{"
            + template
            + "\n"
            + key("NR_GES", episode.overall_no)
            + key("NR_ST", episode.episode_no)
            + key("OT", title)
            + key("Feld1", title_fr)
            + key("REG", director)
            + key("EA", episode.air_date)
            + summary
            + "}}"
        )

    @staticmethod
    def season(season: Season, episode_entries: list[str]) -> str:
        """
        https://de.wikipedia.org/wiki/Vorlage:Episodenlistentabelle
        """
        return (
            f"\n=== Staffel {season.no} ({season.year}) ===\n\n"
            + "{{Episodenlistentabelle|BREITE=100%\n"
            + "| ZUSAMMENFASSUNG = nein\n"
            + "| SORTIERBAR = nein\n"
            + "| REGISSEUR = ja\n"
            + "| DREHBUCH = nein\n"
            + "| Feld1 = Französischer Titel\n"
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


def debug():
    """Test some code"""

    scrapper = FernsehserienScrapper(
        "https://www.fernsehserien.de/arte-360grad-reportage/folgen/606-island-die-wertvollsten-daunen-der-welt-1602943"
    )
    print(scrapper.director)


def scrape():
    for episode in tv_show.episodes:
        if episode.fernsehserien_url:
            scrapper = FernsehserienScrapper(episode.fernsehserien_url)
            print("\n\n" + episode.fernsehserien_url + "\n")
            description = scrapper.description
            if description:
                print(description)
                episode.description = description

            director = scrapper.director
            if director:
                print(director)
                episode.director = director
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


def generate_readme() -> None:
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

    def link_fernsehserien(episode: Episode) -> str:
        if not episode.fernsehserien_episode_no:
            return ""
        return Markdown.link(
            episode.fernsehserien_episode_no, episode.fernsehserien_url
        )

    def link_youtube(episode: Episode) -> str:
        if not episode.youtube_video_id:
            return ""
        return Markdown.link(episode.youtube_video_id, episode.youtube_url)

    def link_imdb(episode: Episode) -> str:
        if not episode.imdb_episode_id:
            return ""
        return Markdown.link(episode.imdb_episode_id, episode.imdb_url)

    def link_thetvdb(episode: Episode) -> str:
        if not episode.thetvdb_season_episode:
            return ""
        return Markdown.link(episode.thetvdb_season_episode, episode.thetvdb_url)

    def format_title(episode: Episode) -> str:
        title: str = episode.title
        if episode.title_fr:
            title += f"<br>fr: *{episode.title_fr}*"
        if episode.title_en:
            title += f"<br>en: *{episode.title_en}*"
        return title

    def format_links(episode: Episode) -> str:
        links: list[str] = []

        def prefix_caption(caption: str, link: str) -> str:
            return f"{caption}: {link}"

        def append(caption: str, link: str | None) -> None:
            if link and link != "":
                links.append(prefix_caption(caption, link))

        if episode.fernsehserien_episode_no:
            append("fernsehserien", link_fernsehserien(episode))

        if episode.thetvdb_season_episode:
            append("thetvdb", link_thetvdb(episode))

        if episode.imdb_episode_id:
            append("imdb", link_imdb(episode))

        if episode.youtube_video_id:
            append("youtube", link_youtube(episode))

        return "<br>".join(links)

    def assemble_row(episode: Episode) -> list[str]:
        row: list[str] = []
        row.append(episode.format_air_date("%a %Y-%m-%d"))
        row.append(format_title(episode))
        row.append(format_links(episode))

        return row

    rows: list[list[str]] = []

    for episode in tv_show.episodes:
        rows.append(assemble_row(episode))

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
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-r", "--readme", action="store_true")
    parser.add_argument("-s", "--scrape", action="store_true")
    parser.add_argument("-w", "--wiki", choices=("de", "fr"))
    parser.add_argument("-y", "--yaml", action="store_true")
    return parser


def main() -> None:
    args = get_argument_parser().parse_args()

    if args.debug:
        debug()

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
