.PHONY: clean dist

all: dist

dist: app
	pyinstaller --onefile main.py

clean:
	rm -rf build dist
