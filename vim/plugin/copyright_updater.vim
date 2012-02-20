" Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

" Copyright updater
"au BufWritePre * call Copyright_updater()

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
			execute '1,'.maxLineno.'!copyright-updater'
	endif

	call CurPos("restore")
endfunction

" Parse the year or years out of a string with years.
function! ParseYears(yearString)
	let years = []

	let commaGroups = split(a:yearString, "\v\s*,\s*")
	echom "commaGroups ".join(commaGroups, "#")

	for commaGroup in commaGroups
		let yearGroup = split(commaGroup, "\v\s*-\s*")
		echom "yearGroup ".join(yearGroup, "#")

		if len(yearGroup) == 1
			let years += yearGroup
		elseif len(yearGroup) == 2
			let years += range(yearGroup[0], yearGroup[-1])
		else
			echom "Cannot parse ".commaGroup
		endif
	endfor

	return years
endfunction
