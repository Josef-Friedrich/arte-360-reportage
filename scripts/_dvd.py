from __future__ import annotations

import typing


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
