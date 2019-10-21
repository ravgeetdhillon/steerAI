import win32api as wapi
import numpy as np
import ctypes
import time
import random


SendInput = ctypes.windll.user32.SendInput

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

NP_2 = 0x50
NP_4 = 0x4B
NP_6 = 0x4D
NP_8 = 0x48

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

w = [1, 0, 0, 0]
a = [0, 1, 0, 0]
d = [0, 0, 1, 0]
nk = [0, 0, 0, 1]

key_list = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789')


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def keys_to_output(keys):
    '''
    Convert the pressed keys to the a boolean value array.
    '''

    output = [0, 0, 0, 0]
    if 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    elif 'W' in keys:
        output = w
    else:
        output = nk
    
    return output


def key_check():
    '''
    Checks the for which keys are pressed.
    '''

    keys = [key for key in key_list if wapi.GetAsyncKeyState(ord(key))]
    return keys


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002,
                        0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def straight():
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)
    ReleaseKey(W)
    PressKey(W)


def left():
    # if random.randrange(0, 3) == 1:
    #     PressKey(W)
    # else:
    #     ReleaseKey(W)
    # ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)
    ReleaseKey(W)
    PressKey(A)


def right():
    # if random.randrange(0, 3) == 1:
    #     PressKey(W)
    # else:
    #     ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)
    ReleaseKey(W)
    PressKey(D)


def nokey():
    # if random.randrange(0, 3) == 1:
    #     PressKey(W)
    # else:
    #     ReleaseKey(W)
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)
    # PressKey(W)
    

# if __name__ == '__main__':
#     PressKey(0x11)
#     time.sleep(1)
#     ReleaseKey(0x11)
#     time.sleep(1)
