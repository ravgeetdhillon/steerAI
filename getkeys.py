import win32api as wapi
import numpy as np

# create a list of inputs that can be given via keyboard for controlling the car
CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789'
key_list = list(CHARACTERS)


def key_check():
    '''
    Checks the for which keys are pressed.
    '''
    keys = [ key for key in key_list if wapi.GetAsyncKeyState( ord(key) ) ]
    return keys
