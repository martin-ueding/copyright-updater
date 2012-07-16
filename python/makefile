# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

###############################################################################
#                                   License                                   #
###############################################################################
# This file is part of copyright updater.
#
# copyright updater is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# copyright updater is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# copyright updater.  If not, see <http://www.gnu.org/licenses/>.

pythonfiles := $(wildcard copyright*.py) copyright-updater
testfiles := $(wildcard *_test.py)

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)

doc:
	epydoc -v $(pythonfiles)
