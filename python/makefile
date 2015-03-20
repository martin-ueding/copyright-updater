# Copyright © 2012-2013, 2015 Martin Ueding <dev@martin-ueding.de>

setupoptions = --prefix "$(DESTDIR)/usr" --install-layout deb

pythonfiles := $(wildcard copyright*.py) copyright-updater
testfiles := $(wildcard *_test.py)

all:

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)

doc:
	epydoc -v $(pythonfiles)

install:
	./setup.py install $(setupoptions)

clean:
	$(RM) *.pyc
	$(RM) -r build
	$(RM) copyright-updaterc
