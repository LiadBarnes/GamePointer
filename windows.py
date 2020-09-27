import win32gui
import win32ui
from PIL import Image, ImageDraw
from pip._vendor.colorama.win32 import windll

class Windows:
    def __init__(self, app_name):
        self.hwnd = win32gui.FindWindow(None, app_name)
        self.update_window_properties()

    def update_window_properties(self):
        x0, y0, x1, y1 = win32gui.GetWindowRect(self.hwnd)
        self.x = x0
        self.y = y0
        self.w = x1 - x0
        self.h = y1 - y0

    def screenshot(self, filename='test', crop=None):

        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, self.w, self.h)

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 1)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        if crop:
            im = im.crop(crop)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)

        draw = ImageDraw.Draw(im)
        left, top, right, bottom = 600, 50, 600, 200
        draw.line((left, top, right, bottom), fill=128)

        if result == 1:
            # PrintWindow Succeeded
            im.save(f"{filename}.png")

    def move_to_zero(self):
        win32gui.MoveWindow(self.hwnd, 0, 0, self.w, self.h, True)
        self.update_window_properties()


#app = Windows('BlueStacks')
#app.screenshot()
