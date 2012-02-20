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

	let maxLineno = min([line("$"), 5])

	" Check whether the current year is already in the header. If so, there is
	" no need to call the copyright updater. If there is no copyright string,
	" no need to call it either.
	let hasYear = 0
	let hasCopyright = 0
	for i in range(1, maxLineno)
		if match(getline(i), strftime('%Y')) >= 0
			let hasYear = 1
			break
		endif
		if match(getline(i), 'Copyright') >= 0
			let hasCopyright = 1
		endif
	endfor

	" If the current year is not in the header and the file is modified, call
	" the copyright updater.
	if !hasYear && hasCopyright && &modified
			%!copyright-updater
			python main()
	endif

	call CurPos("restore")
endfunction

