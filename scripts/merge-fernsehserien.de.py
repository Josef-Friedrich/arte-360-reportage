#! /usr/bin/env python

import typing
from lxml import etree

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

    output = []

    for episode in root:
        slag_line = get_text(episode, "url")

        e = {
            "no": int(get_text(episode, "no")),
            "air_date": get_text(episode, "date"),
            "title": get_text(episode, "title"),
            "slag_line": slag_line,
            "id": int(re.sub(r".*-", "", slag_line)),
        }
        output.append(e)

    return output


if __name__ == "__main__":
    fernsehserien = parseXML("fernsehserien.de.xml")
    print(fernsehserien)
