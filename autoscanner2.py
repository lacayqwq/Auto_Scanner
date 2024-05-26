# import mss
# import cv2
# from pyzbar.pyzbar import decode
# import time
# import keyboard
# import sys
# from tkinter import messagebox
# import winsound
# def capture_and_check_qr():
#     with mss.mss() as sct:
#         print("开始检测画面")
#         while True:
#             for monitor_number, monitor in enumerate(sct.monitors[1:], 1):
#                 screenshot = sct.shot(mon=monitor_number)
                
#                 # 使用OpenCV加载图像
#                 img = cv2.imread(screenshot)

#                 # 灰度化
#                 gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#                 # 检测二维码
#                 qr_codes = decode(gray_img)
                
#                 for qr in qr_codes:
#                     print(f"在显示器 {monitor_number} 的截图中检测到二维码: {qr.data.decode()}")
#                     winsound.Beep(1000, 3000)
#                     messagebox.showwarning('警告','有码！')
#                 if qr_codes:
#                     print("退出进程")
#                     sys.exit()

#             # 检查是否按下 'Ctrl+Q' 组合键
#             if keyboard.is_pressed('ctrl+q'):
#                 print("程序已退出")
#                 break

#             # 等待3秒
#             time.sleep(0.5)

# def main():
#     capture_and_check_qr()

# if __name__ == '__main__':
#     main()
import mss
import cv2
from pyzbar.pyzbar import decode
import time
import keyboard
import sys
from tkinter import messagebox
import winsound
import threading

# 用于线程协同工作的事件对象
exit_event = threading.Event()

def show_warning():
    messagebox.showwarning('警告', '有码！')

def capture_and_check_qr():
    with mss.mss() as sct:
        print("开始检测画面")
        while not exit_event.is_set():
            for monitor_number, monitor in enumerate(sct.monitors[1:], 1):
                screenshot = sct.shot(mon=monitor_number)
                
                # 使用OpenCV加载图像
                img = cv2.imread(screenshot)

                # 灰度化
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # 检测二维码
                qr_codes = decode(gray_img)
                
                for qr in qr_codes:
                    print(f"在显示器 {monitor_number} 的截图中检测到二维码: {qr.data.decode()}")
                    winsound.Beep(1000, 3000)
                    threading.Thread(target=show_warning).start()
                    exit_event.set()
                    break
                if qr_codes:
                    break

            # 检查是否按下 'Ctrl+Q' 组合键
            if keyboard.is_pressed('ctrl+q'):
                print("程序已退出")
                exit_event.set()
                break

            # 等待0.5秒
            time.sleep(0.5)

def main():
    capture_thread = threading.Thread(target=capture_and_check_qr)
    capture_thread.start()
    capture_thread.join()  # 等待线程结束

if __name__ == '__main__':
    main()
