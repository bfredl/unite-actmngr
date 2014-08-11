let s:save_cpo = &cpo
set cpo&vim

function! unite#kinds#activity#define() "{{{
  return s:kind
endfunction"}}}

let s:kind = {
      \ 'name' : 'activity',
      \ 'action_table': {},
      \ 'default_action' : 'activate',
      \}

" Actions "{{{
let s:kind.action_table.activate = {
      \ 'description' : 'activate this window',
      \ }

function! s:kind.action_table.activate.func(candidate) "{{{
    call actmngr#activate(a:candidate.action__actid)
endfunction"}}}
"}}}

let &cpo = s:save_cpo
unlet s:save_cpo

" vim: foldmethod=marker
