all: json readme wiki

json:
	./script.py --json

readme:
	./scripts/generate-readme.py

wiki:
	./scripts/generate-wikitext.py
	./scripts/generate-wikitext-fr.py
