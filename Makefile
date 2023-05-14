all: json readme wiki

json:
	./scripts/export-to-json.py

readme:
	./scripts/generate-readme.py

wiki:
	./scripts/generate-wikitext.py
