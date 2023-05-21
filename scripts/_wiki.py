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


def __format_titel_ergaenzung(episode: Episode) -> str:
    return f"zur Folge „{episode.title}“"


def format_ref_imdb(episode: Episode) -> str:
    "https://developer.imdb.com/documentation/key-concepts"
    if not episode.imdb_url or not episode.imdb_episode_id:
        return ""
    return format_ref(
        format_internetquelle(
            url=episode.imdb_url,
            titel=f"Episoden-ID (title entity): {episode.imdb_episode_id}",
            titel_ergaenzung=__format_titel_ergaenzung(episode),
            herausgeber="Internet Movie Database (IMDb)",
            website="imdb.com",
        )
    )


def format_ref_fernsehserien(episode: Episode) -> str:
    if (
        not episode.fernsehserien_episode_no
        or not episode.fernsehserien_episode_slug
        or not episode.fernsehserien_episode_id
        or not episode.fernsehserien_url
    ):
        return ""
    return format_ref(
        format_internetquelle(
            url=episode.fernsehserien_url,
            titel=f"Fortlaufende-Nr.: {episode.fernsehserien_episode_no}, Episoden-ID: {episode.fernsehserien_episode_id}",
            titel_ergaenzung=__format_titel_ergaenzung(episode),
            herausgeber="imfernsehen GmbH & Co. KG",
            website="fernsehserien.de",
        )
    )
