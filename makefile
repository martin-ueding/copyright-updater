# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

all:

install:
	cd python && python setup.py install --root "$(DESTDIR)" --install-layout deb
	install -d "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/copyright_updater.py -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/copyright_updater.vim -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/curpos.vim -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"

clean:
	make -C python clean
