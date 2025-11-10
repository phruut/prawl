import win32gui
import win32con
import win32api
import win32process
import win32com.client

def find():
    hwnd = win32gui.FindWindow(None, 'Brawlhalla')
    if hwnd:
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
            proc_name = win32process.GetModuleFileNameEx(handle, 0)
            if 'brawlhalla.exe' in proc_name.lower():
                return hwnd
        except:
            pass
    return None

def running():
    return bool(find())

def show(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW) if hwnd else None

def hide(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE) if hwnd else None

def visible(hwnd):
    return win32gui.IsWindowVisible(hwnd) if hwnd else False

def activate(hwnd):
    # for some reason you need to press alt key before activating a window...? what the helly
    shell = win32com.client.Dispatch('WScript.Shell'); shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd) if hwnd else None

def close():
    hwnd = find()
    if hwnd:
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
            win32api.TerminateProcess(handle, 0)
            win32api.CloseHandle(handle)
        except:
            pass
