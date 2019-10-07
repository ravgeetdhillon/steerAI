from screen import screenshot, show_image
from keys import keys_to_output, key_check
import numpy as np
import cv2
import time
import os

SCREEN_GRAB_WIDTH = 800
SCREEN_GRAB_HEIGHT = 600
RESIZE_FACTOR = 0.5
SAVE_POINT = 500


def setup():
    '''
    Setup the project space for storing the data.
    '''

    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/dataset'):
        os.mkdir('data/dataset')

    starting_value = 1
    while True:
        if not os.path.exists(f'data/dataset/part{starting_value}'):
            os.mkdir(f'data/dataset/part{starting_value}')
            part = f'part{starting_value}'
            break
        else:
            starting_value += 1

    starting_value = 1
    while True:
        file_name = f'data/dataset/{part}/training_data-{starting_value}.npy'
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

            # grabs the screen, resizes it and then converts in to Grayscale mode
            screen = screenshot(
                region=(10, 40, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT))
            scaled_width = int(SCREEN_GRAB_WIDTH * RESIZE_FACTOR)
            scaled_height = int(SCREEN_GRAB_HEIGHT * RESIZE_FACTOR)
            screen = cv2.resize(screen, (scaled_width, scaled_height))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            # # records the key presses for each image
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
                file_name = f'data/dataset/{part}/training_data-{starting_value}.npy'

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
