import Xlib
from Xlib import X, Xatom, Xutil, display
from Xlib.protocol import event
from collections import namedtuple
from subprocess import call
atoms = [
        "_NET_CLIENT_LIST",
        "_NET_WM_NAME",
        "_NET_WM_DESKTOP",
        "_NET_ACTIVE_WINDOW",
        "_NET_CURRENT_DESKTOP",
        "_NET_WM_STATE",
        "_NET_WM_STATE_HIDDEN",
        ]

XTask = namedtuple('XTask',['wid','title','desktop'])

class XWinMgr(object):
    def __init__(self):
        self.disp = display.Display()
        self.scr = self.disp.screen()
        self.root = self.scr.root
        for a in atoms:
            setattr(self, a, self.disp.intern_atom(a))

    def get_clients(self):
        tasks = self.root.get_full_property(self._NET_CLIENT_LIST, Xatom.WINDOW).value
        l = []
        for wid in tasks:
            o = self.disp.create_resource_object("window", wid)
            name = o.get_full_property(self._NET_WM_NAME, 0)
            if not name:
                name = o.get_full_property(Xatom.WM_NAME, 0)
            title = name.value
            desktop = o.get_full_property(self._NET_WM_DESKTOP, Xatom.CARDINAL).value[0]
            l.append( XTask(wid,title,desktop) )
        return l

    def get_active_window(self):
        return self.root.get_full_property(self._NET_ACTIVE_WINDOW, Xatom.WINDOW).value[0]

    def iconify(self, win):
        #self.setEwmhProp(win, self._NET_WM_STATE, [1, self._NET_WM_STATE_HIDDEN, 0, 1])
        call(['xdotool','windowminimize', str(win)])

    def set_sticky(self, win):
        call(['wmctrl', '-r', str(win), '-b', 'add,sticky'])

    def activate(self, wid, movedesktop=False):
        if movedesktop:
            desk = self.root.get_full_property(self._NET_CURRENT_DESKTOP, Xatom.CARDINAL).value
            call(['xdotool','set_desktop_for_window', str(wid), str(desk[0])])
        call(['xdotool','windowactivate',str(wid)])
        if False:
            o = self.disp.create_resource_object("window", wid)
            self.setEwmhProp(o, self._NET_ACTIVE_WINDOW, [1, X.CurrentTime, wid])
            if desktop is not None:
                self.setEwmhProp(self.root, self._NET_CURRENT_DESKTOP, [int(desktop), X.CurrentTime])

    def setEwmhProp(self, win, prop, data, mask=None):
        if type(data) is str:
            dataSize = 8
        else:
            data = (data+[0]*(5-len(data)))[:5]
            dataSize = 32
        
        ev = event.ClientMessage(window=win, client_type=prop, data=(dataSize, data))

        if not mask:
            mask = (X.SubstructureRedirectMask|X.SubstructureNotifyMask)
        self.root.send_event(ev, event_mask=mask)
        self.disp.pending_events()


