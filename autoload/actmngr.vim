let s:SourcedFile=expand("<sfile>")
python <<EOF
import vim, sys
from os.path import join, dirname
fpath = vim.eval("s:SourcedFile")
pydir = join(dirname(dirname(fpath)),"python")
print pydir
sys.path.append(pydir)

from xutil import XWinMgr
wm = XWinMgr()

def actmngr_get_activites():
    tasks = wm.get_clients()
    return [ { 'desc': t.title, 'id':t.wid } for t in tasks ]

def actmngr_activate(id):
    wid = int(id)
    wm.activate(wid)
EOF

function! actmngr#get_activities()
    return pyeval("actmngr_get_activites()")
endfunction

function! actmngr#activate(id)
    python actmngr_activate(vim.eval("a:id"))
endfunction


