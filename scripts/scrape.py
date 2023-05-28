#! /usr/bin/env python

import re

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

URL = "https://www.fernsehserien.de/arte-360grad-reportage/folgen/1-traum-staedte-beirut-die-milliarden-dollar-utopie-339116"
MARKER = "-*-*-*-"


def scrape(url: str) -> BeautifulSoup:
    page = requests.get(url)
    return BeautifulSoup(page.content, "lxml")


def extract_text(element: Tag | NavigableString | None) -> str | None:
    if element:
        text = str(element)
        text = re.sub(' *<br/?> *', MARKER, text)
        text = BeautifulSoup(text, 'lxml').text
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        text = text.replace(MARKER, '\n\n')
        return text


def get_description(soup: BeautifulSoup) -> str | None:
    element: Tag | NavigableString | None = soup.find("div", class_="episode-output-inhalt-inner")
    return extract_text(element)


content = get_description(scrape(url=URL))
print(content)
