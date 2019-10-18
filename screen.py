from variables import RESIZE_FACTOR
import numpy as np
import cv2
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
        screen = screenshot(region=(10, 40, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT))
        scaled_width = int(SCREEN_GRAB_WIDTH * RESIZE_FACTOR)
        scaled_height = int(SCREEN_GRAB_HEIGHT * RESIZE_FACTOR)
        screen = cv2.resize(screen, (scaled_width, scaled_height))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    cv2.imshow('gray_image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def gaussian_blur(img, kernel_size):
    '''
    Applies a Gaussian Noise kernel.
    '''

    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def isolate_color_mask(img, low_thresh, high_thresh):
    assert(low_thresh.all() >=0  and low_thresh.all() <=255)
    assert(high_thresh.all() >=0 and high_thresh.all() <=255)
    return cv2.inRange(img, low_thresh, high_thresh)


def adjust_gamma(image, gamma=1.0):
    '''
    Darkens the image.
    '''

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)


def to_hls(img):
    '''
    Converts RGB image to HSL image.
    '''

    return cv2.cvtColor(img, cv2.COLOR_RGB2HLS)


def to_gray(img):
    '''
    Converts RGB image to Grayscale image.
    '''

    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def convert_image(image):
    '''
    Converts the image to the desired format by passing it through a transformation pipeline.
    '''

    original = np.copy(image)

    # phase 1
    image1 = np.copy(original)
    image1 = to_gray(image1)
    image1 = adjust_gamma(image1, 0.5)

    # phase 2
    image2 = np.copy(original)
    white_mask = isolate_color_mask(image2, np.array([210, 210, 210, 255], dtype=np.uint8), np.array([255, 255, 255, 255], dtype=np.uint8))
    yellow_mask = isolate_color_mask(image2, np.array([190, 190, 0, 255], dtype=np.uint8), np.array([255, 255, 255, 255], dtype=np.uint8))
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    image2 = cv2.bitwise_and(image1, image1, mask=mask)

    # phase 3
    image3 = np.copy(original)
    white_mask = isolate_color_mask(to_hls(image3), np.array([0, 200, 0], dtype=np.uint8), np.array([200, 255, 255], dtype=np.uint8))
    yellow_mask = isolate_color_mask(to_hls(image3), np.array([10, 0, 100], dtype=np.uint8), np.array([40, 255, 255], dtype=np.uint8))
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    image3 = cv2.bitwise_and(image1, image1, mask=mask)

    final = cv2.bitwise_and(image2, image3)
    final = gaussian_blur(final, kernel_size=5)

    # resize the image for better computational performance
    height, width = final.shape
    scaled_width = int(width * RESIZE_FACTOR)
    scaled_height = int(height * RESIZE_FACTOR)
    final = cv2.resize(final, (scaled_width, scaled_height))
    final = final[(scaled_height//3):-(scaled_height//10), ]

    return np.array(final)
