from __future__ import annotations

from datetime import date
import typing
import re

import typing_extensions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _lib import TvShowData


class EpisodeData(typing.TypedDict):
    title: str
    """German title"""

    alias: str
    title_fr: str
    """French title"""

    title_en: str
    """English title"""

    air_date: str

    duration: int

    season: int

    episode: int

    thetvdb_season_episode: str

    thetvdb_episode_id: int

    fernsehserien_air_date: str

    fernsehserien_episode_no: int
    """for example ``117``"""

    fernsehserien_episode_slug: str
    """for example ``117-die-bernsteintaucher-339440``"""

    fernsehserien_episode_id: int
    """for example ``339440``"""

    imdb_episode_id: str

    youtube_video_id: str

    index: typing_extensions.NotRequired[int]


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
    def title_fr(self) -> str | None:
        if "title_fr" in self.data and self.data["title_fr"] != "":
            return self.data["title_fr"]

    @property
    def title_en(self) -> str | None:
        if "title_en" in self.data and self.data["title_en"] != "":
            return self.data["title_en"]

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
    def season_no(self) -> int | None:
        return self.__get_season_or_episode(False)

    @property
    def episode_no(self) -> int | None:
        return self.__get_season_or_episode(True)

    @property
    def year(self) -> int:
        return int(self.data["air_date"][0:4])
