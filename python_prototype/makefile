# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles := $(wildcard *.py)
testfiles := $(wildcard *_test.py)

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)
