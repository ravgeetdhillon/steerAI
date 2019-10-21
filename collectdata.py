from variables import SCREEN_GRAB_START_WIDTH, SCREEN_GRAB_START_HEIGHT, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT, RESIZE_FACTOR, SAVE_POINT
from screen import screenshot, show_image
from keys import keys_to_output, key_check, w, a, d, nk
import numpy as np
import cv2
import time
import os


def setup():
    '''
    Setup the project space for storing the data.
    '''

    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/raw_dataset'):
        os.mkdir('data/raw_dataset')

    starting_value = 1
    while True:
        if not os.path.exists(f'data/raw_dataset/part{starting_value}'):
            os.mkdir(f'data/raw_dataset/part{starting_value}')
            part = f'part{starting_value}'
            break
        else:
            starting_value += 1

    starting_value = 1
    while True:
        file_name = f'data/raw_dataset/{part}/training_data-{starting_value}.npy'
        if not os.path.isfile(file_name):
            print(f'STARTING WITH VALUE : {starting_value}')
            break
        else:
            starting_value += 1

    return (file_name, part, starting_value)


def are_equal(data):
    '''
    Checks whether all the elements in the data are equal.
    '''

    if all(i[1] == data[0][1] for i in data):
        return True
    else:
        return False


def main():

    # gives a countdown before starting the process
    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)
    print('START')

    # load the important variables
    paused = False
    file_name, part, starting_value = setup()
    lefts, rights, straights, nokeys, training_data = [], [], [], [], []

    count = 0
    last_time = time.time()

    # a buffer to store the screenshots and key presses
    # used to remove the accidentally pressed keys
    # helps in keeping the data accurate and clean
    buffer = []

    while True:
        if not paused:

            # checks the number of images processed per seconds
            count += 1
            now = time.time()
            if now - last_time >= 1:
                print(f'-FPS {count}')
                count = 0
                last_time = now

            # grabs the screen in the given region
            screen = screenshot(
                region=(SCREEN_GRAB_START_WIDTH, SCREEN_GRAB_START_HEIGHT, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT))

            # records the key presses for each image
            keys = key_check()
            output = keys_to_output(keys)

            print(f'nk:{len(nokeys)},lefts:{len(lefts)},rights:{len(rights)},straights:{len(straights)}')
            
            # add the data to buffer if the current action is same as the actions in the buffer
            if len(buffer) == 0 or buffer[-1][1] == output:
                buffer.append( [screen, output] )
                continue
            
            # flush the buffer if keypresses dont last longer
            # keys have been pressed to orient the vehicle a little bit but weren't necessary
            elif len(buffer) < 2 and buffer[-1][1] != output:
                buffer = []
                continue
            
            elif len(buffer) >= 2 and buffer[-1][1] != output:
                if buffer[-1][1] == a:
                    while len(lefts) < SAVE_POINT // 4 and len(buffer) > 0:
                        lefts.append( buffer.pop() )
                
                elif buffer[-1][1] == d:
                    while len(rights) < SAVE_POINT // 4 and len(buffer) > 0:
                        rights.append( buffer.pop() )
                
                elif buffer[-1][1] == w:
                    while len(straights) < SAVE_POINT // 4 and len(buffer) > 0:
                        straights.append( buffer.pop() )
                
                elif buffer[-1][1] == nk:
                    while len(nokeys) < SAVE_POINT // 4 and len(buffer) > 0:
                        nokeys.append( buffer.pop() )
                
            buffer = [ [screen, output] ]

            # store the data into the npy file after the dataset size reaches images specified in `SAVE_POINT`
            if sum([len(lefts), len(rights), len(straights), len(nokeys)]) == SAVE_POINT:
                training_data = lefts + rights + straights + nokeys
                np.save(file_name, training_data)
                print(f'-----SAVED {starting_value}-----')
                lefts, rights, straights, nokeys, training_data = [], [], [], [], []
                starting_value += 1
                file_name = f'data/raw_dataset/{part}/training_data-{starting_value}.npy'

        # press `T` to stop the data collection process
        keys = key_check()
        if 'T' in keys:
            if paused:
                print('STARTING AGAIN')
                paused = False
            else:
                print('PAUSED')
                paused = True
            time.sleep(1)


main()
