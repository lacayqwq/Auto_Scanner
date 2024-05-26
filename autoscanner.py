import win32gui
import win32con
import win32process
from PIL import Image, ImageGrab
from pyzbar.pyzbar import decode
import win32api

def list_windows():
    titles = []
    def enum_window_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            titles.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_window_callback, None)
    return titles

def get_window_pos(hwnd):
    return win32gui.GetWindowRect(hwnd), hwnd

def get_monitors():
    monitors = []
    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        monitors.append(win32api.GetMonitorInfo(hMonitor))
    win32api.EnumDisplayMonitors(None, None, monitor_enum_proc)
    return monitors

def fetch_image(hwnd):
    (x1, y1, x2, y2), handle = get_window_pos(hwnd)
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # win32process.AllowSetForegroundWindow(win32process.GetCurrentProcessId())
    # try:
    #     win32gui.SetForegroundWindow(handle)
    # except Exception as e:
    #     print(f"Error setting foreground: {e}")
    # Consider multiple monitors: coordinates may need adjustments if monitors are arranged left/right
    grab_image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    return grab_image

def detect_qr_code(image):
    results = decode(image)
    if results:
        print("检测到二维码:")
        for result in results:
            print(f"数据: {result.data.decode()}，类型: {result.type}")
    else:
        print("未检测到二维码")

def main():
    monitors = get_monitors()
    print("Connected Monitors:", [monitor['Monitor'] for monitor in monitors])
    windows = list_windows()
    for i, (hwnd, title) in enumerate(windows):
        print(f"{i}: {title}")
    choice = int(input("请选择一个窗口进行截图: "))
    hwnd = windows[choice][0]
    image = fetch_image(hwnd)
    image.show()
    detect_qr_code(image)

if __name__ == '__main__':
    main()
