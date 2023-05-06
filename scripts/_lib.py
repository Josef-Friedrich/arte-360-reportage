import yaml
import typing
import difflib


class Episode(typing.TypedDict):
    title: str
    air_date: str
    duration: int
    thetvdb_season_episode: str
    thetvdb_episode_no: int


class Geo(typing.TypedDict):
    episodes: list[Episode]
    databases: dict[str, str]


geo: Geo | None = None


def load() -> Geo:
    global geo
    if geo:
        return geo
    with open("360-grad-reportage.yml", "r") as y:
        result = yaml.load(y, Loader=yaml.Loader)
        geo = result
        return result


geo = load()

titles: list[str] = []
for episode in geo["episodes"]:
    titles.append(episode["title"])


def get_episode_by_title(title: str | None) -> Episode | None:
    if not title:
        return
    match: list[str] = difflib.get_close_matches(title, titles, n=1)
    if len(match) > 0:
        return geo["episodes"][titles.index(match[0])]
