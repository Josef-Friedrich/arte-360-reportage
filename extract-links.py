#! /usr/bin/env python

import re

file = open("Sheet1.html", "r")

content = file.read()

for match in re.finditer(r"/episodes/([0-9]+)\".*?>(.*?)<", content, re.DOTALL):
    print(match.group(1))
