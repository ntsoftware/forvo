.PHONY: clean dist lint test

all: dist

lint:
	ruff check --statistics

test:
	pytest

dist:
	pyinstaller main.spec

clean:
	rm -rf build dist
