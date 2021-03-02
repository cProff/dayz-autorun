import keyboard
import win32api
import time

class AutoRunner():

    def __init__(self, hotkey) -> None:
        self.hotkey = hotkey
        self.isRunning = False

    def switch_mode(self):
        if keyboard.is_pressed('shift+w'):
            self.isRunning = False
            win32api.keybd_event(0x57, win32api.MapVirtualKey(0x57, 0), 0x0002, 0)  # w
            win32api.keybd_event(0xA0, win32api.MapVirtualKey(0xA0, 0), 0x0002, 0)  # shift
        else:
            self.isRunning = True
            win32api.keybd_event(0x57, win32api.MapVirtualKey(0x57, 0), 0, 0)  # w
            win32api.keybd_event(0xA0, win32api.MapVirtualKey(0xA0, 0), 0, 0)  # shift

    def stop(self, key):
        if self.isRunning:
            keyboard.press_and_release(key)
            self.isRunning = False

    def enable(self):
        keyboard.on_press_key(self.hotkey, lambda e: self.switch_mode())
        keyboard.on_release_key('w', lambda e: self.stop('shift'))
        keyboard.on_release_key('shift', lambda e: self.stop('w'))
        # keyboard.wait(self.hotkeyExit)
    
    def disable(self):
        keyboard.unhook_all()