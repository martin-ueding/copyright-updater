" Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

" Copyright updater
au BufWritePre * call Copyright_updater()

" Import the Python module into this namespace.
let s:basename = fnamemodify(expand('<sfile>'), ':h')
let s:basename = s:basename.'/copyright_updater.py'
execute 'pyfile '.s:basename

" This is called before writing
function! Copyright_updater()
	if &modified
		call CurPos("save")
		python update_copyright()
		call CurPos("restore")
	endif
endfunction
