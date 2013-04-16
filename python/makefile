# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

pythonfiles := $(wildcard copyright*.py) copyright-updater
testfiles := $(wildcard *_test.py)

all:

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)

doc:
	epydoc -v $(pythonfiles)

install:
	./setup.py install --prefix "$(DESTDIR)/usr" --install-layout deb

clean:
	$(RM) *.pyc
	$(RM) -r build
	$(RM) copyright-updaterc
