all: json readme wiki yaml

json:
	./arte-360-reportage.py --json

readme:
	./arte-360-reportage.py --readme

wiki:
	./arte-360-reportage.py --wiki de
	./arte-360-reportage.py --wiki fr

yaml:
	./arte-360-reportage.py --yaml
