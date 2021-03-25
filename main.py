import wx.adv
import wx
from plyer import notification
import proccheck
import autorun
import config
from bindata import resource_path
from updater import download_release, have2update
import os
import subprocess

import keyboard


TRAY_TOOLTIP = 'DayZ AutoRun'
TRAY_ICON = 'icon-white.ico'
PROCESS_NAME = 'DayZ_x64.exe'
VERSION = 'v0.2'
REPO = 'cproff/dayz-autorun'


def notify(text, timeout=3, force=False):
    if not config.SETTINGS['silence'] or force:
        notification.notify(
            title=TRAY_TOOLTIP,
            message=text,
            app_icon=resource_path(TRAY_ICON),
            timeout=timeout)

def create_menu_item(menu, label, func):
    item = menu.AppendSubMenu(None, label, help="")
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    # menu.Append(item)
    return item

class BindInput(wx.TextCtrl):
    def __init__(self, *args, hotkey=None, isOneKey=False, **kw):
        super().__init__(*args, style=wx.TE_READONLY, **kw)
        if hotkey:
            self.set_hotkey(hotkey)
        self.isOneKey = isOneKey
        self.Bind(wx.EVT_LEFT_DOWN, lambda e: self.read_hotkey())

    def set_hotkey(self, text):
        self.Clear()
        self.AppendText(text)
    
    def read_hotkey(self):
        self.Clear()
        self.AppendText('Recording...')
        if self.isOneKey:
            shortcut = keyboard.read_key(False)
        else:
            shortcut = keyboard.read_hotkey(False)
        self.set_hotkey(shortcut)

class Block(wx.Panel):
    def __init__(self, parent, label, *args, **kw):
        super().__init__(parent, *args, **kw)
        sb = wx.StaticBox(self, label=label)
        self.sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        self.SetSizer(self.sbs)
    
    def add(self, input, label='Hotkey:'):
        box = wx.BoxSizer(wx.HORIZONTAL)
        # self.sbs.Add(input, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=5)
        box.Add(wx.StaticText(self, label=label), flag=wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)
        box.Add(input, flag=wx.BOTTOM, border=5)
        self.sbs.Add(box)

class SettingsDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.InitUI()
        self.SetTitle("Settings")
        self.menu = None

    def InitUI(self):
        blockAutorun = Block(self, 'Autorun')
        self.bindAutorun = BindInput(blockAutorun, hotkey=config.get_param('autorun_hk'), isOneKey=True)
        self.checkAutorun = wx.CheckBox(blockAutorun)
        self.checkAutorun.SetValue(config.get_param('autorun_state'))
        blockAutorun.add(self.bindAutorun)
        blockAutorun.add(self.checkAutorun, label='Activated: ')

        blockDwarfglitch = Block(self, 'Dwarf glitch')
        self.bindDwarfglitch = BindInput(blockDwarfglitch, hotkey=config.get_param('dwarfglitch_hk'))
        self.checkDwarfglitch = wx.CheckBox(blockDwarfglitch)
        self.checkDwarfglitch.SetValue(config.get_param('dwarfglitch_state'))
        blockDwarfglitch.add(self.bindDwarfglitch)
        blockDwarfglitch.add(self.checkDwarfglitch, label='Activated: ')

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.applyBtn = wx.Button(self, label='Apply')
        # # self.applyBtn.Enable(False)
        hbox2.Add(self.applyBtn)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(blockAutorun, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(blockDwarfglitch, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizer(vbox)

        self.applyBtn.Bind(wx.EVT_BUTTON, self.OnApply)


    def OnApply(self, e):
        config.set_param('autorun_hk', self.bindAutorun.GetValue())
        config.set_param('dwarfglitch_hk', self.bindDwarfglitch.GetValue())
        config.set_param('autorun_state', self.checkAutorun.GetValue())
        config.set_param('dwarfglitch_state', self.checkDwarfglitch.GetValue())
        self.Destroy()

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        self.autorunHK = autorun.AutoRunner(config.get_param('autorun_hk'), config.get_param('dwarfglitch_hk'))
        super().__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_config)

        self.onGo = True
        self.dayzState = None
        if self.onGo:
            wx.CallLater(1000, self.on_timer)

    def CreatePopupMenu(self):
        self.menu = wx.Menu()
        create_menu_item(self.menu, 'Settings', self.on_config)
        self.menu.AppendSeparator()
        create_menu_item(self.menu, f'Status: {"ON" if self.onGo else "OFF"}', self.start_switch)
        create_menu_item(self.menu, f'Silence: {"ON" if config.get_param("silence") else "OFF"}', self.silence_switch)
        self.menu.AppendSeparator()
        create_menu_item(self.menu, 'Exit', self.on_exit)
        return self.menu

    def start_switch(self, e):
        self.onGo = not self.onGo
        if self.onGo:
            wx.CallLater(1000, self.on_timer)
        else:
            self.dayzState = False
            self.autorunHK.disable()
        self.menu.UpdateUI()

    def silence_switch(self, e):
        config.set_param('silence', not config.SETTINGS["silence"])

    def set_icon(self, path):
        icon = wx.Icon(resource_path(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_config(self, e):
        self.autorunHK.disable()
        dlg = SettingsDialog(self.frame)
        dlg.ShowModal()
        self.autorunHK.hkAutorun = config.get_param('autorun_hk')
        self.autorunHK.hkDwarfglitch = config.get_param('dwarfglitch_hk')
        self.autorunHK.enable(config.get_param('autorun_state'), config.get_param('dwarfglitch_state'))

    def on_timer(self):
        if not self.onGo:
            return
        newState = proccheck.process_exists(PROCESS_NAME)
        if self.dayzState != newState:
            if newState:
                self.autorunHK.enable(config.get_param('autorun_state'), config.get_param('dwarfglitch_state'))
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
            print(cmdline)
            # os.system(cmdline)
            subprocess.Popen(cmdline, shell=True)
            return
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
