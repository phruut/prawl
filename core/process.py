import time
import psutil
import win32gui
import win32con
import win32api
import win32process
import win32com.client

import logging
logger = logging.getLogger('prawl')

class Process:
    def __init__(self, config):
        self.config = config
        self.process_name = config.network.get('process', 'executable')
        self.window_title = config.network.get('process', 'window_title')
        self._pid: int | None = None
        self._hwnd: int | None = None
        self._last_check = 0.0
        self.cache_timeout = 1.0  # seconds

    def _update(self):
        if time.time() - self._last_check < self.cache_timeout:
            return
        self._last_check = time.time()

        pid = None
        exe_path = None
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            if proc.info['name'] == self.process_name:
                pid = proc.info['pid']
                exe_path = proc.info['exe']
                break

        hwnd = None
        if pid:
            # main check
            hwnd = win32gui.FindWindow(None, self.window_title)
            if hwnd:
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid != pid:
                    hwnd = None

            # fallback
            if not hwnd:
                def enum_cb(h, result):
                    if win32gui.GetWindowText(h):
                        _, p = win32process.GetWindowThreadProcessId(h)
                        if p == pid:
                            result.append(h)
                    return True

                results = []
                win32gui.EnumWindows(enum_cb, results)
                for h in results:
                    if win32gui.IsWindowVisible(h):
                        hwnd = h
                        break
                if not hwnd and results:
                    hwnd = results[0]

        self._pid = pid
        self._hwnd = hwnd

        if pid and exe_path:
            logger.debug(f'process found! pid {pid} | hwnd {hwnd} | path {exe_path}')

    def get_pid(self):
        self._update()
        logger.debug(f'get pid: {self._pid}')
        return self._pid

    def get_hwnd(self):
        self._update()
        logger.debug(f'get hwnd: {self._hwnd}')
        return self._hwnd

    def running(self):
        self._update()
        logger.debug('check process running')
        return self._pid is not None

    def show(self):
        hwnd = self.get_hwnd()
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            logger.info(f'show window | hwnd: {hwnd}')

    def hide(self):
        hwnd = self.get_hwnd()
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            logger.info(f'hide window | hwnd: {hwnd}')

    def visible(self):
        hwnd = self.get_hwnd()
        logger.debug('check process visibility')
        return win32gui.IsWindowVisible(hwnd) if hwnd else False

    def activate(self):
        hwnd = self.get_hwnd()
        if hwnd:
            shell = win32com.client.Dispatch('WScript.Shell')
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(hwnd)
            logger.debug('activate process window')

    def close(self):
        pid = self.get_pid()
        if pid:
            try:
                handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
                win32api.TerminateProcess(handle, 0)
                win32api.CloseHandle(handle)
                logger.info(f'terminated brawlhalla | pid: {pid}')
            except Exception as e:
                logger.exception(f'failed to terminate: {e}')
            finally:
                self._pid = None
                self._hwnd = None
