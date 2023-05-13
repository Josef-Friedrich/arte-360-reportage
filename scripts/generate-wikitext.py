#! /usr/bin/env python

from __future__ import annotations


from _lib import geo_360 as geo

"""
https://de.wikipedia.org/wiki/Vorlage:Episodenlistentabelle
https://de.wikipedia.org/wiki/Vorlage:Episodenlisteneintrag
"""

rows: list[str] = []
for episode in geo.episodes:
    print(episode.episode_no)
    rows.append(episode.wikitext)


content = (
    """{{Episodenlistentabelle|BREITE=100%
| ZUSAMMENFASSUNG = nein
| SORTIERBAR = nein
| REGISSEUR = nein
| DREHBUCH= nein
| INHALT =
"""
    + "\n".join(rows)
    + "\n}}"
)


with open("360-grad-reportage.wikitext", "w") as readme:
    readme.write(content)
