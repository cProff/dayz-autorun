import keyboard
import win32api
import time

def win_press(keycode):
    win32api.keybd_event(keycode, win32api.MapVirtualKey(keycode, 0), 0, 0)

def win_release(keycode):
    win32api.keybd_event(keycode, win32api.MapVirtualKey(keycode, 0), 0x0002, 0)

def win_press_release(keycode, dt=0.2):
    win_press(keycode)
    time.sleep(dt)
    win_release(keycode)


class AutoRunner():

    def __init__(self, hkAutorun, hkDwarfglitch) -> None:
        self.hkAutorun = hkAutorun
        self.hkDwarfglitch = hkDwarfglitch
        self.isRunning = False
        self.letRelease = {'shift':False, 'w':False}

    def switch_mode(self):
        if self.isRunning:
            self.isRunning = False
            win_release(0x57)  # w
            win_release(0xA0)  # shift
        else:
            self.letRelease['w'] = keyboard.is_pressed('w')
            self.letRelease['shift'] = keyboard.is_pressed('shift')
            self.isRunning = True
            win_press(0x57)  # w
            win_press(0xA0)  # shift

    def forse_release(self):
        win_release(0x57)  # w
        win_release(0xA0)  # shift

    def stop(self, key):
        if self.isRunning and key in self.letRelease and self.letRelease[key]:
            self.letRelease[key] = False
            if key == 'w':
                win_press(0x57)  # w
            elif key == 'shift':
                win_press(0xA0)  # shift
        elif self.isRunning:
            self.forse_release()
            self.isRunning = False

    def enable(self, autorunState, dwarfglitchState):
        if autorunState:
            keyboard.on_press_key(self.hkAutorun, lambda e: self.switch_mode())
            keyboard.on_release_key('w', lambda e: self.stop('w'))
            keyboard.on_release_key('shift', lambda e: self.stop('shift'))
            keyboard.on_release_key('s', lambda e: self.stop('s'))
        if dwarfglitchState:
            keyboard.add_hotkey(self.hkDwarfglitch, lambda: self.go_dwarf())
    
    def disable(self):
        self.forse_release()
        keyboard.unhook_all()

    def go_dwarf(self):
        for i in range(10):
            win_press(0x47)  # G
            time.sleep(0.07)
            win_press(0x77)  # f8
            time.sleep(0.05)
            win_release(0x47)  # G
            win_release(0x77)  # f8
            time.sleep(0.05)