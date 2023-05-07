import yaml
import typing
import difflib
import termcolor


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


def read_text_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


geo = load()

titles: list[str] = []
for episode in geo["episodes"]:
    titles.append(episode["title"])


def normalize_title(title: str) -> str:
    title = title.replace(", ", " ")
    title = title.replace(": ", " ")
    title = title.replace(" - ", " ")
    return title.lower()


def get_episode_by_title(title: str | None, debug: bool = False) -> Episode | None:
    if not title:
        return
    match: list[str] = difflib.get_close_matches(title, titles, n=1)
    episode = None
    if len(match) > 0:
        episode = geo["episodes"][titles.index(match[0])]

    if debug:
        if not episode:
            print(f"No match found for: {termcolor.colored(title, color='red')}")
        elif normalize_title(title) != normalize_title(episode["title"]):
            print(
                f"{termcolor.colored(title, color='yellow')} <> {termcolor.colored(episode['title'], color='blue')}"
            )

    return episode


def get_episode_index_by_title(title: str) -> int:
    return titles.index(title)
