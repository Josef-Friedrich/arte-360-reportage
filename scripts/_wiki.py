import datetime
from _lib import Episode


def format_ref(content: str | None) -> str:
    if not content:
        return ""
    return "<ref>" + content + "</ref>"


def format_internetquelle(url: str, titel: str, abruf: str | None = None) -> str:
    def format_key_value(key: str, value: str) -> str:
        return "|" + key + "=" + value

    entries: list[str] = []

    def append(key: str, value: str) -> None:
        entries.append(format_key_value(key, value))

    append("url", url)
    append("titel", titel)

    if not abruf:
        abruf = datetime.date.today().isoformat()
    append("abruf", abruf)

    markup: str = " ".join(entries)
    return "{{Internetquelle " + markup + "}}"


def format_ref_imdb(episode: Episode) -> str:
    if not episode.imdb_url or not episode.imdb_episode_id:
        return ""

    titel: str = "IMDB-Episoden-ID: " + episode.imdb_episode_id
    return format_internetquelle(url=episode.imdb_url, titel=titel)
