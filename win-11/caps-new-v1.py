#-------------------------------------------------------------------------------
# Name:        caps on/off
import ctypes
from time import sleep
import keyboard
def send_ctrl_alt_0_user():
    keyboard.write("xxxxxx")
def send_ctrl_alt_9_passwd():
    keyboard.press_and_release('ctrl+alt+9')
    keyboard.write("xxxxxx")
def send_ctrl_alt_8_code():
    keyboard.write("xxxxxx")
def send_ctrl9():
    keyboard.write(mmmmm)
def send_ctrl0():
    keyboard.write("xxxxxx")
# Register hotkeys
keyboard.add_hotkey("ctrl+9", send_ctrl9)
keyboard.add_hotkey("ctrl+0", send_ctrl0)
keyboard.add_hotkey('ctrl+alt+0', send_ctrl_alt_0_user)
keyboard.add_hotkey('ctrl+alt+8', send_ctrl_alt_8_code)
keyboard.add_hotkey('ctrl+alt+9', send_ctrl_alt_9_passwd)
def caps(toggle=1):
    VK_CAPITAL = 0x14
    ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 0X0002, 0)
    sleep(.1)
    ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 0, 0)
    ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 0X0002, 0)
def main():
    hllDll = ctypes.WinDLL ("User32.dll")
    while True:
        caps()
        sleep(180)
    pass
if __name__ == '__main__':
    main()
#-------------------------------------------------------------------------------