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

all:
	@echo "Nothing to do."

install:
	cd python && python setup.py install --prefix "$(DESTDIR)"
	install -d "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/copyright_updater.py -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/copyright_updater.vim -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/curpos.vim -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
