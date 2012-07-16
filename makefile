# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all:
	@echo "Nothing to do."

install:
	cd python && python setup.py install --prefix "$(DESTDIR)"
	install -d "$(DESTDIR)/usr/share/vim/addons/plugin/"
	install -m 644 vim/plugin/copyright_updater.py -t "$(DESTDIR)/usr/share/vim/addons/plugin/"
	install -m 644 vim/plugin/copyright_updater.vim -t "$(DESTDIR)/usr/share/vim/addons/plugin/"
	install -m 644 vim/plugin/curpos.vim -t "$(DESTDIR)/usr/share/vim/addons/plugin/"
