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

statefile = "/tmp/renamethisfile"

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
        tasks = self.wm.get_clients()
        with state() as s:
            # FIXME: task labels type unstable
            return [ { 'desc': t.title, 'id': t.wid, 'hotkey': s.get(str(t.wid),{}).get('hotkey') } for t in tasks ]

    def activate(self, task):
        wid = int(task)
        try:
            self.wm.activate(wid)
        except:
            call(['xdotool','windowactivate',str(task)])

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


