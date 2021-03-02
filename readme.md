# DayZ AutoRun

This is a simplest autorun app for any DayZ SA server. It will allow you use custom hotkey for autorun as if server has autorun mod (but DayZ window must still be active and of course you cant manage your loot on the go). It is not a cheat because all it does is pushing W+Shift all the time.

#### Installation

This app doesn't need any installation, just download last release from the [releases page](https://github.com/cProff/dayz-autorun/releases) and save it in some folder. On first execution it'll create file "param.ini" and that's all. Now you can play DayZ and enjoy your autorun. 

###### Windows startup

It is on your own, but starting this app every time computer starts is a little lazily. You can add it to the Windows startup and **DayZ_AutoRun** will starts with Windows. To do it you need make following steps:

1. Press WIN+R,  write "shell:startup" and press ENTER
2. Create Windows link for **DayZ_AutoRun** in opened folder:
   - Mouse right-click on executable, "create link"
   - Copy created link to the folder

Now **DayZ_AutoRun** is added to the Windows startup list. 

#### Usage

Usage is pretty simple. First of all setup the hotkey, default is numpad-plus (as for server mode). It can be done by mouse left-click on tray icon of **DayZ_AutoRun** or by choosing *config hotkey* in tray dropdown menu. Now **DayZ_AutoRun** is ready to work.

If you don't want **DayZ_AutoRun** to send you notification every time it save your chair from your ass-fire, you can set *silence* parameter to OFF. 

#### How it works

This app create a hotkey that will press W and Shift buttons when DayZ_64.exe is running. Against all other autorun apps (like AHK scripts) this one will stop pushing buttons if you wanna run by yorself.