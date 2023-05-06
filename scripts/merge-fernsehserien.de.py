#! /usr/bin/env python

import typing
from lxml import etree

import _lib

import re


def get_text(element: typing.Any, tag: str):
    elements = element.xpath(tag)
    if len(elements) != 1:
        print(element)
        raise Exception("not found")
    return elements[0].text.strip()


def parseXML(xmlFile: str):
    """
    Parse the xml
    """
    with open(xmlFile) as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)

    output: list[dict[str, int | str]] = []

    for episode in root:
        slug = get_text(episode, "url")

        e: dict[str, int | str] = {
            "no": int(get_text(episode, "no")),
            "air_date": get_text(episode, "date"),
            "title": get_text(episode, "title"),
            "slug": slug,
            "id": int(re.sub(r".*-", "", slug)),
        }
        output.append(e)

    return output


def normalize_title(title: str) -> str:
    title = title.replace(", ", " ")
    title = title.replace(": ", " ")
    title = title.replace(" - ", " ")
    return title.lower()


if __name__ == "__main__":
    fernsehserien = parseXML("fernsehserien.de.xml")

    geo = _lib.load()

    for e in fernsehserien:
        src = str(e["title"])
        episode = _lib.get_episode_by_title(src)
        dest = ""
        if episode:
            dest = episode["title"]

            index = _lib.get_episode_index_by_title(dest)

            episode["fernsehserien_episode_slug"] = str(e["slug"])
            episode["fernsehserien_episode_no"] = int(e["id"])

            geo["episodes"][index] = episode

        if normalize_title(src) != normalize_title(dest):
            print("s", src)
            print("d", dest)
            print()

    #_lib.write(geo)
