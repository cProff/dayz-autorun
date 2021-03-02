import wx.adv
import wx
from plyer import notification
import proccheck
import autorun
import config
from bindata import resource_path
from updater import download_release, have2update
import os

import keyboard


TRAY_TOOLTIP = 'DayZ AutoRun'
TRAY_ICON = 'icon-white.ico'
PROCESS_NAME = 'DayZ_x64.exe'
VERSION = 'v0.1'
REPO = None #'cproff/wzfix'


def notify(text, timeout=3, force=False):
    if not config.SETTINGS['silence'] or force:
        notification.notify(
            title=TRAY_TOOLTIP,
            message=text,
            app_icon=resource_path(TRAY_ICON),
            timeout=timeout)

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class BindingDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.InitUI()
        self.SetSize((250, 150))
        self.SetTitle("Setup hotkey")

    def InitUI(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Autorun hotkey')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        self.text = wx.TextCtrl(pnl,style=wx.TE_READONLY)
        self.text.AppendText(config.get_param('hotkey'))
        sbs.Add(self.text, flag=wx.CENTER, border=5)

        pnl.SetSizer(sbs)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.applyBtn = wx.Button(self, label='Apply')
        self.applyBtn.Enable(False)
        hbox2.Add(self.applyBtn)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        self.applyBtn.Bind(wx.EVT_BUTTON, self.OnApply)
        self.text.Bind(wx.EVT_LEFT_DOWN, self.bind_update)

    def bind_update(self, e):
        self.text.Clear()
        self.text.AppendText('Recording...')
        shortcut = keyboard.read_hotkey(False)
        self.text.Clear()
        self.text.AppendText(shortcut)
        self.applyBtn.Enable()

    def OnApply(self, e):
        config.set_param('hotkey', self.text.GetValue())
        self.Destroy()

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        self.autorunHK = autorun.AutoRunner(config.get_param('hotkey'))
        super().__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_config)

        self.onGo = True
        self.dayzState = None
        if self.onGo:
            wx.CallLater(1000, self.on_timer)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Config hotkey', self.on_config)
        menu.AppendSeparator()
        create_menu_item(menu, f'Status: {"ON" if self.onGo else "OFF"}', self.start_switch)
        create_menu_item(menu, f'Silence: {"ON" if config.SETTINGS["silence"] else "OFF"}', self.silence_switch)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def start_switch(self, e):
        self.onGo = not self.onGo
        if self.onGo:
            wx.CallLater(1000, self.on_timer)
        else:
            self.dayzState = False
            self.autorunHK.disable()

    def silence_switch(self, e):
        config.set_param('silence', not config.SETTINGS["silence"])

    def set_icon(self, path):
        icon = wx.Icon(resource_path(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_config(self, e):
        dlg = BindingDialog(self.frame)
        dlg.ShowModal()
        self.autorunHK.hotkey = config.get_param('hotkey')

    def on_timer(self):
        if not self.onGo:
            return
        newState = proccheck.process_exists(PROCESS_NAME)
        if self.dayzState != newState:
            if newState:
                self.autorunHK.enable()
                notify('Autorun is ready.')
            elif not self.dayzState is None:
                self.autorunHK.disable()
                notify('Autoran is stopped.')
        self.dayzState = newState
        wx.CallLater(1000, self.on_timer)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        exit()

class App(wx.App):
    def OnInit(self):
        config.load()
        TaskBarIcon(None)
        return True


def main():
    if have2update(REPO, VERSION):
        print('updating')
        updated, cmdline = download_release(REPO, VERSION)
        if updated:
            os.popen(cmdline)
            return
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
