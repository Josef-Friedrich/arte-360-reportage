all: json readme

json:
	./scripts/export-to-json.py

readme:
	./scripts/generate-readme.py
