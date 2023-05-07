import yaml
import typing
import difflib
import termcolor


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
    index: int


class GeoMetaData(typing.TypedDict):
    episodes: list[Episode]
    databases: dict[str, str]


geo: GeoMetaData | None = None

YAML_FILENAME = "360-grad-reportage.yml"


def load() -> GeoMetaData:
    global geo
    if geo:
        return geo
    with open(YAML_FILENAME, "r") as y:
        result: GeoMetaData = yaml.load(y, Loader=yaml.Loader)

        i: int = 0
        for episode in result["episodes"]:
            episode["index"] = i

            i += 1

        geo = result
        return result


def write(geo: GeoMetaData) -> None:
    with open(YAML_FILENAME, "w") as y:
        yaml.dump(geo, stream=y, allow_unicode=True, sort_keys=False)


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
        self.data = load()

        self.titles = {}
        for episode in self.data["episodes"]:
            self.titles[episode["title"]] = episode["index"]
            if "alias" in episode:
                self.titles[episode["alias"]] = episode["index"]
            if "title_fr" in episode:
                self.titles[episode["title_fr"]] = episode["index"]
            if "title_en" in episode:
                self.titles[episode["title_en"]] = episode["index"]

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

    def save(self) -> None:
        write(self.data)


geo_360 = Geo360()
