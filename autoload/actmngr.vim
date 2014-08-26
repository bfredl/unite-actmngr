let s:SourcedFile=expand("<sfile>")
python <<EOF
import vim, sys, cStringIO
from os.path import join, dirname
fpath = vim.eval("s:SourcedFile")
pydir = join(dirname(dirname(fpath)),"python")
sys.path.append(pydir)
import actmngr
m  = sys.stdout
sys.stdout = cStringIO.StringIO()
am = actmngr.ActivityManager()
# in case gvim this will be wrong, fixed in GuiEnter
mywid = am.wm.get_active_window()
sys.stdout = m
def actmngr_get_tasks():
    tasks = am.get_tasks()
    res = [{ 'desc': "{:>2} {}".format(t.get("hotkey") or "", t["desc"]), 'id': t['id'] } for t in tasks]
    return res

EOF
function! actmngr#on_gui_enter()
    python mywid = am.wm.get_active_window()
endfunction

function! actmngr#on_buflist_update()
    python actmngr.dump_buflist(vim, mywid)
endfunction

function! actmngr#switch_to_buf(bufid)
    let g:tbuf = a:bufid
    exe "b".a:bufid
endfunction

function! actmngr#get_tasks()
    return pyeval("actmngr_get_tasks()")
endfunction

function! actmngr#activate(id)
    python am.activate(vim.eval("a:id"))
endfunction

function! actmngr#set_hotkey(id,...)
    if a:0 > 0
        let key = a:1
    else
        let key = input("hotkey: ")
    endif
    python am.set_hotkey(vim.eval("a:id"),vim.eval("key"))
endfunction

function! s:switcher_app_settings()
    inoremap <buffer><expr> <c-t> unite#do_action('hotkey')
    noremap <buffer><expr> <c-t> unite#do_action('hotkey')
endfunction

function! actmngr#switcher_app()
    python mywid = am.wm.get_active_window()
    python am.set_switcher(mywid)
    au FileType unite call <sid>switcher_app_settings()
    au FocusLost * python am.wm.iconify(mywid)
    call actmngr#activate_switcher()
endfunction

function! actmngr#activate_switcher()
    Unite -buffer-name=tasks -no-split activities
    python am.wm.activate(mywid)
endfunction
