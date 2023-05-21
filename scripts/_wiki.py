import datetime
from _lib import Episode


def format_ref(content: str | None) -> str:
    if not content or content == "":
        return ""
    return "<ref>" + content + "</ref>"


def format_internetquelle(
    url: str,
    titel: str,
    abruf: str | None = None,
    website: str | None = None,
    titel_ergaenzung: str | None = None,
    herausgeber: str | None = None,
) -> str:
    """https://de.wikipedia.org/wiki/Vorlage:Internetquelle"""

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
        abruf = datetime.date.today().isoformat()
    append("abruf", abruf)

    markup: str = " ".join(entries)
    return "{{Internetquelle " + markup + "}}"


def format_ref_imdb(episode: Episode) -> str:
    "https://developer.imdb.com/documentation/key-concepts"
    if not episode.imdb_url or not episode.imdb_episode_id:
        return ""

    titel: str = "Episoden-ID (title entity): " + episode.imdb_episode_id
    return format_ref(
        format_internetquelle(
            url=episode.imdb_url,
            titel=titel,
            herausgeber="Internet Movie Database (IMDb)",
            website="imdb.com",
        )
    )
