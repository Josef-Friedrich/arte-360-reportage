#! /usr/bin/env python

import json
import _lib

with open("360-grad-reportage.json", "w") as j:
    json.dump(_lib.load(), fp=j, indent=2, ensure_ascii=False)
