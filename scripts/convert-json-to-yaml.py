#! /usr/bin/env python

import yaml
import json


with open("geo.json", "r") as j:
    result = json.load(j)

with open("geo.yaml", "w") as y:
    yaml.dump(result, stream=y, allow_unicode=True, sort_keys=False)
