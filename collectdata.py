from variables import SCREEN_GRAB_START_WIDTH, SCREEN_GRAB_START_HEIGHT, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT, RESIZE_FACTOR, SAVE_POINT
from screen import screenshot, show_image
from keys import keys_to_output, key_check
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


def main():

    # gives a countdown before starting the process
    for i in list(range(2))[::-1]:
        print(i + 1)
        time.sleep(1)
    print('START')

    # load the important variables
    paused = False
    file_name, part, starting_value = setup()
    training_data = []

    count = 0
    last_time = time.time()

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

            # stores the pixel data of the image and the corresponding key presses in the training data array
            training_data.append([screen, output])

            # regular checkpoints to keep the track of data collection process
            if len(training_data) % 100 == 0:
                print('--MILESTONE REACHED')

            # store the data into the npy file after the dataset size reaches 500 images
            if len(training_data) == SAVE_POINT:
                np.save(file_name, training_data)
                print(f'-----SAVED {starting_value}-----')
                training_data = []
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
