from __future__ import annotations

import re


def read_text_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def clean_title(title: str) -> str:
    title = title.replace("–", "-")
    title = re.sub(r" *\(.+\) *", " ", title)
    title = title.strip()
    title = re.sub(r"  +", " ", title)
    title = re.sub(r"GEO Reportage *[:-] +", "", title)
    title = re.sub(r"^\d+ *- *", "", title)
    return title


def normalize_title(title: str) -> str:
    title = title.replace(", ", " ")
    title = title.replace(": ", " ")
    title = title.replace(" - ", " ")
    return title.lower()
