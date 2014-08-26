
augroup Actmngr
    au! BufAdd * call actmngr#on_buflist_update()
    au! BufFilePost * call actmngr#on_buflist_update()
    au! BufDelete * call actmngr#on_buflist_update()
    au! VimLeave * python actmngr.delete_buflist(vim)
    au! GuiEnter * call actmngr#on_gui_enter()
augroup END
