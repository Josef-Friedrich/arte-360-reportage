SCRIPT = .venv/bin/arte-360-reportage.py

all:
	$(SCRIPT) --all

summary:
	$(SCRIPT) --summary

coordinates:
	$(SCRIPT) --coordinates

directors:
	$(SCRIPT) --directors

dvd:
	$(SCRIPT) --dvd

json:
	$(SCRIPT) --json

kartographer:
	$(SCRIPT) --kartographer

leaflet:
	$(SCRIPT) --leaflet
	xdg-open karte.html

readme:
	$(SCRIPT) --readme

tmp:
	$(SCRIPT) --tmp

wiki:
	$(SCRIPT) --wiki de
	$(SCRIPT) --wiki fr

yaml:
	$(SCRIPT) --yaml

install:
	poetry install
