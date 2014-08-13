let s:save_cpo = &cpo
set cpo&vim

function! unite#sources#activities#define() "{{{
  return s:source
endfunction"}}}

let s:source = {
      \ 'name' : 'activities',
      \ 'description' : 'open windows',
      \ 'action_table' : {},
      \ 'default_kind' : 'activity',
      \}

function! s:source.gather_candidates(args, context) "{{{
    let tasks = actmngr#get_tasks()

  return map(tasks, "{
        \ 'word' : v:val.desc,
        \ 'action__actid' : v:val.id
        \ }")
endfunction"}}}
