all: json readme wiki

json:
	./script.py --json

readme:
	./script.py --readme

wiki:
	./script.py --wiki de
	./script.py --wiki fr
