let s:SourcedFile=expand("<sfile>")
python <<EOF
import vim, sys
from os.path import join, dirname
fpath = vim.eval("s:SourcedFile")
pydir = join(dirname(dirname(fpath)),"python")
print pydir
sys.path.append(pydir)

from actmngr import ActivityManager
am = ActivityManager()
def actmngr_get_tasks():
    tasks = am.get_tasks()
    res = [{ 'desc': "{:>2} {}".format(t.get("hotkey") or "", t["desc"]), 'id': t['id'] } for t in tasks]
    return res

EOF

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


