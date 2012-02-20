" Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

" Copyright updater
"au BufWritePre * call Copyright_updater()

let s:basename = fnamemodify(expand('<sfile>'), ':h')
echom s:basename

let s:basename = s:basename.'/copyright_updater.py'
echom s:basename

execute 'pyfile '.s:basename

function! Copyright_updater()
	call CurPos("save")

	python update_copyright()

	call CurPos("restore")
endfunction
