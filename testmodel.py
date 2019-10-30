from variables import SCREEN_GRAB_START_WIDTH, SCREEN_GRAB_START_HEIGHT, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT
from keys import straight, left, right
from tensorflow.keras import models
from screen import screenshot, show_image
import numpy as np
import time
import tensorflow as tf
import numpy as np
import sys
import cv2


MODEL_NAME = 'sdc-cnn-model.h5'
print(f'Loading Model: {MODEL_NAME}')
model = tf.keras.models.load_model(MODEL_NAME)


def get_action(image):
    
    print('1')
    image = cv2.resize(image, None, fx=0.5, fy=0.5)
    print('2')
    image = tf.cast(image, tf.float32)
    print('3')

    prediction = model.predict(np.array([image])).tolist()[0]
    print(prediction)
    choice = prediction.index( max(prediction) )
    print(choice)
    if choice == 0:
        choice = 'straight'
    elif choice == 1:
        choice = 'left'
    elif choice == 2:
        choice = 'right'
    
    return choice


def main():

    # gives a countdown before starting the process
    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)
    print('START')

    # load the important variables
    paused = False
    last_time = time.time()

    while True:
        if not paused:

            # checks the time taken to to process each image
            now = time.time()
            print(f'-Time {round(now - last_time, 4)}')
            last_time = now

            # grabs the screen, resizes it and then converts in to Grayscale mode
            screen = screenshot(region=(SCREEN_GRAB_START_WIDTH, SCREEN_GRAB_START_HEIGHT, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT))
            
            response = get_action(screen)

            if response == 'straight':
                straight()

            elif response == 'left':
                left()
                
            elif response == 'right':
                right()

            print(response)

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

# main()

image = cv2.imread('img/image292-straight.png')
# show_image(image)
a = get_action(image)
print(a)