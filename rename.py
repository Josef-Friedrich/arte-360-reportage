#! /usr/bin/python

import re
import glob
import os


for rel_path in glob.glob("**/**"):
    old_path = rel_path
    rel_path = rel_path.replace("GEO Reportage - ", "")
    rel_path = rel_path.replace("(360° GEO Reportage)", "")
    rel_path = rel_path.replace("(ARTE 360° Reportage)", "")
    rel_path = rel_path.replace(" - ", " ")
    rel_path = rel_path.replace("  ", " ")
    segments: list[str] = rel_path.split("/")

    subfolder: str = segments[0]
    file_name = segments[1]

    file_name = re.sub(r"-(\w{11})\.(\w+)$", r" (YT \1).\2", file_name)

    if re.match(r"^S\d\dE\d\d", file_name):
        file_name = re.sub(r"S(\d\d)E(\d\d)", r"s\1e\2", file_name)

    if re.match(r"^\d\d ", file_name, flags=re.I):
        file_name = subfolder + "e" + file_name

    new_path = subfolder + "/" + file_name
    new_path = new_path.replace("  ", " ")

    if new_path != old_path:
        print(new_path + " <- " + old_path)
        os.rename(old_path, new_path)
