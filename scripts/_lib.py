import yaml
import typing
import difflib


class Episode(typing.TypedDict):
    title: str
    air_date: str
    duration: int
    thetvdb_season_episode: str
    thetvdb_episode_id: int
    fernsehserien_air_date: str
    fernsehserien_episode_no: int
    fernsehserien_episode_slug: str
    fernsehserien_episode_id: int


class Geo(typing.TypedDict):
    episodes: list[Episode]
    databases: dict[str, str]


geo: Geo | None = None

YAML_FILENAME = "360-grad-reportage.yml"


def load() -> Geo:
    global geo
    if geo:
        return geo
    with open(YAML_FILENAME, "r") as y:
        result = yaml.load(y, Loader=yaml.Loader)
        geo = result
        return result


def write(geo: Geo) -> None:
    with open(YAML_FILENAME, "w") as y:
        yaml.dump(geo, stream=y, allow_unicode=True, sort_keys=False)


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


def get_episode_index_by_title(title: str) -> int:
    return titles.index(title)
