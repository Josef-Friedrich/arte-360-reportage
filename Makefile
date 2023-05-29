SCRIPT = .venv/bin/arte-360-reportage.py

all: chatgpt json readme wiki yaml

chatgpt:
	$(SCRIPT) --chatgpt

debug:
	$(SCRIPT) --debug

json:
	$(SCRIPT) --json

readme:
	$(SCRIPT) --readme

wiki:
	$(SCRIPT) --wiki de
	$(SCRIPT) --wiki fr

yaml:
	$(SCRIPT) --yaml

install:
	poetry install
