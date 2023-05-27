from __future__ import annotations

import typing


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from _episode import EpisodeData


class SeasonData(typing.TypedDict):
    no: int
    year: int
    episodes: list[EpisodeData]
