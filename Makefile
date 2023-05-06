all: json readme

json:
	./scripts/convert-yml-to-json.py

readme:
	./scripts/generate-readme.py
