# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

all:

install:
	install -d "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/copyright_updater.py -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/copyright_updater.vim -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	install -m 644 vim/plugin/curpos.vim -t "$(DESTDIR)/usr/share/vim/vimfiles/plugin/"
	make -C python install

clean:
	make -C python clean
