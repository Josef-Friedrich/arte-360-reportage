all: json readme wiki

json:
	./script.py --json

readme:
	./script.py --readme

wiki:
	./scripts/generate-wikitext.py
	./scripts/generate-wikitext-fr.py
