SCRIPT = .venv/bin/arte-360-reportage.py

all: chatgpt json leaflet readme wiki yaml

chatgpt:
	$(SCRIPT) --chatgpt

coordinates:
	$(SCRIPT) --coordinates:

json:
	$(SCRIPT) --json

leaflet:
	$(SCRIPT) --leaflet

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
