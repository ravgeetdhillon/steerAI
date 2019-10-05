import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import win32api


def screenshot(region=None):
    '''
    Grabs the screenshot of the given region.
    '''

    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img


def show_image(image=None, grab=False):
    '''
    Displays the given image.
    If grab is set to `True`, then a screenshot of region is taken and is shown as well.
    '''

    if grab:
        screen = grab_screen(
            region=(10, 40, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT))
        scaled_width = int(SCREEN_GRAB_WIDTH * RESIZE_FACTOR)
        scaled_height = int(SCREEN_GRAB_HEIGHT * RESIZE_FACTOR)
        screen = cv2.resize(screen, (scaled_width, scaled_height))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    cv2.imshow('gray_image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
