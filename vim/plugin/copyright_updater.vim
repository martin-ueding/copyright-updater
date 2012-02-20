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

" http://vim.wikia.com/wiki/Maintain_cursor_and_screen_position
function CurPos(action)
  if a:action == "save"
    let b:saveve = &virtualedit
    let b:savesiso = &sidescrolloff
    set virtualedit=all
    set sidescrolloff=0
    let b:curline = line(".")
    let b:curvcol = virtcol(".")
    let b:curwcol = wincol()
    normal! g0
    let b:algvcol = virtcol(".")
    normal! M
    let b:midline = line(".")
    execute "normal! ".b:curline."G".b:curvcol."|"
    let &virtualedit = b:saveve
    let &sidescrolloff = b:savesiso
  elseif a:action == "restore"
    let b:saveve = &virtualedit
    let b:savesiso = &sidescrolloff
    set virtualedit=all
    set sidescrolloff=0
    execute "normal! ".b:midline."Gzz".b:curline."G0"
    let nw = wincol() - 1
    if b:curvcol != b:curwcol - nw
      execute "normal! ".b:algvcol."|zs"
      let s = wincol() - nw - 1
      if s != 0
        execute "normal! ".s."zl"
      endif
    endif
    execute "normal! ".b:curvcol."|"
    let &virtualedit = b:saveve
    let &sidescrolloff = b:savesiso
    unlet b:saveve b:savesiso b:curline b:curvcol b:curwcol b:algvcol b:midline
  endif
  return ""
endfunction
