#! /usr/bin/env python

import yaml
import json


with open("360-grad-reportage.yml", "r") as y:
    result = yaml.load(y, Loader=yaml.Loader)

with open("360-grad-reportage.json", "w") as j:
    json.dump(result, fp=j, indent=2, ensure_ascii=False)
