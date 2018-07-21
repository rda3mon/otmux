all: otmux

clean: 
	rm -rf MANIFEST build/ dist/
	find . -name "*.pyc" -delete

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

otmux: otmux/*.py
	mkdir -p zip
	for d in otmux ; do \
		mkdir -p zip/$$d ;\
		cp -pPR $$d/*.py zip/$$d/ ;\
	done
	touch -t 200001010101 zip/otmux/*.py
	mv zip/otmux/__main__.py zip/
	cd zip ; zip -q ../otmux otmux/*.py __main__.py
	rm -rf zip
	echo '#!$(PYTHON)' > otmux
	cat otmux.zip >> otmux
	rm otmux.zip
	chmod a+x otmux
