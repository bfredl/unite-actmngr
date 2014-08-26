from __future__ import print_function, division
from os.path import dirname
from contextlib import contextmanager
from subprocess import call
import os,sys
import json
import tempfile
try:
    import xutil
except:
    pass

def ensuredir(dname):
    if not os.path.exists(dname):
        os.makedirs(dname)
    return dname

rtdir = ensuredir(os.path.join(os.environ["XDG_RUNTIME_DIR"],'actmngr'))

statefile = os.path.join(rtdir, "state")

@contextmanager
def Persistent(fn, mode='r', empty=dict):
    try:
        with open(fn,'r') as f:
            contents = f.read()
            data = json.loads(contents)
    except IOError:
        data = empty()
    yield data
    if mode == 'w':
        js = json.dumps(data)
        with tempfile.NamedTemporaryFile(
                'w', dir=dirname(fn), delete=False) as tf:
            tf.write(js)
            tempname = tf.name
        os.rename(tempname, fn)

def state(mode='r'):
    return Persistent(statefile, mode)

class ActivityManager(object):
    def __init__(self):
        try:
            self.wm = xutil.XWinMgr()
        except:
            pass

    def get_tasks(self):
        wins = self.wm.get_clients()
        tasks = []
        with state() as s:
            # FIXME: task labels type unstable
            for w in wins:
                tid = "win:{}".format(w.wid)
                ts = s.get(tid,{})
                if ts.get('is_switcher'): 
                    continue
                tasks.append( { 'desc': w.title, 'id': tid, 'hotkey': ts.get('hotkey') } )
            for b in self.get_buffers():
                tid = "vim:" + b['name']
                ptid = "win:{}".format( b['wid'])
                ts = s.get(tid,{})
                tasks.append({ 'desc': b['name'], 'id': tid, 'parent': ptid, 'hotkey': ts.get('hotkey') } )
        return tasks

    def activate(self, task):
        kind, id = task.split(':',1)
        if kind == "win":
            self.wm.activate(int(id))
        elif kind == "vim":
            # FIXME: fix this
            for b in self.get_buffers():
                if b['name'] == id:
                    print(b)
                    self.wm.activate(int(b['wid']))
                    call(['vim', '--servername', b['srv'], '--remote-expr', 'actmngr#switch_to_buf({})'.format(b['nbr'])])
                    break


    def get_buffers(self):
        for f in os.listdir(vimdir):
            dat = json.load(open(os.path.join(vimdir, f)))
            for buf in dat:
                yield buf


    def get_hotkeys(self):
        with state() as s:
            return {v["hotkey"]:k for (k,v) in s.items() if v.get("hotkey") is not None}

    def set_hotkey(self, task, hotkey):
        """
        @type s: dict
        """
        with state('w') as s:
            #remove duplicate
            for k,v in s.items():
                if v.get("hotkey") == hotkey:
                    del v["hotkey"]
            s.setdefault(task,{})["hotkey"] = hotkey

    def set_switcher(self, task):
        with state('w') as s:
            s.setdefault(task,{})["is_switcher"] = True

vimdir = ensuredir(os.path.join(rtdir, 'vim'))
def dump_buflist(vim, wid):
    srvname = vim.eval("v:servername")
    pid = str(vim.eval('getpid()'))
    blist = []
    for b in vim.buffers:
        if not b.options['buflisted'] or not b.name:
            continue
        blist.append( { 'srv': srvname, 'wid': wid, 'nbr': b.number, 'name': b.name } )
    with tempfile.NamedTemporaryFile(
                'w', dir=rtdir, delete=False) as tf:
        json.dump(blist,tf)
        tempname = tf.name
    os.rename(tempname, os.path.join(vimdir,pid))

def delete_buflist(vim):
    pid = str(vim.eval('getpid()'))
    try:
        os.unlink(os.path.join(vimdir, pid))
    except:
        pass
