# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles := $(wildcard copyright*.py)
testfiles := $(wildcard *_test.py)

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)

doc:
	epydoc -v $(pythonfiles)
