" Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

" Copyright updater
"au BufWritePre * call Copyright_updater()

" Import thy Python module into this namespace.
let s:basename = fnamemodify(expand('<sfile>'), ':h')
echom s:basename

let s:basename = s:basename.'/copyright_updater.py'
echom s:basename

execute 'pyfile '.s:basename

" This is called before writing
function! Copyright_updater()
	call CurPos("save")

	python update_copyright()

	call CurPos("restore")
endfunction
