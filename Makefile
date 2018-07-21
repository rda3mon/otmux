PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
PYTHON ?= /usr/bin/env python

all: otmux/*.py
	mkdir -p dist
	mkdir -p dist/zip
	for d in otmux ; do \
		mkdir -p dist/zip/$$d ;\
		cp -pPR $$d/*.py dist/zip/$$d/ ;\
	done
	touch -t 200001010101 dist/zip/otmux/*.py
	mv dist/zip/otmux/__main__.py dist/zip/
	cd dist/zip ; zip -q ../otmux otmux/*.py __main__.py
	rm -rf dist/zip
	echo '#!$(PYTHON)' > dist/otmux
	cat dist/otmux.zip >> dist/otmux
	rm dist/otmux.zip
	chmod a+x dist/otmux

clean:
	rm -rf MANIFEST build/ dist/
	find . -name "*.pyc" -delete

