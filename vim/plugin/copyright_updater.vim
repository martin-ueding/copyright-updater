" Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

" Copyright updater
au BufWritePre * call Copyright_updater()

function! Copyright_updater()
	call CurPos("save")

	let lineno = min([line("$"), 5])

	" Check whether the current year is already in the header. If so, there is
	" no need to call the copyright updater.
	let hasYear = 0
	for i in range(1, lineno)
		if match(getline(i), strftime('%Y')) >= 0
			let hasYear = 1
			break
		endif
	endfor

	" If the current year is not in the header and the file is modified, call
	" the copyright updater.
	if !hasYear && &modified
			%!copyright-updater
			execute '1,'.lineno.'!copyright-updater'
	endif

	call CurPos("restore")
endfunction
