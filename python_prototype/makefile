# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

testfiles := $(wildcard *_test.py)

test:
	python -m doctest *.py
	python -m unittest $(testfiles:.py=)
