from keys import W, A, S, D, straight, left, right, nokey, keys_to_output, key_check
from variables import SCREEN_GRAB_START_WIDTH, SCREEN_GRAB_START_HEIGHT, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT
from screen import screenshot, convert_image
import numpy as np
import time


def get_action(image):
    
    image = convert_image(image)

    image = np.ndarray.flatten(image)

    weightage = {
        'lefts': 0,
        'rights': 0,
        'straights': 0,
        'nokeys': 0,
    }

    for key in ['straights', 'lefts', 'rights', 'nokeys']:
        weightage[key] = np.sum( model[key]['weights'] * image )

    predicted_action = max(weightage.keys(), key=(lambda key: weightage[key]))

    return predicted_action


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

            if response == 'straights':
                straight()

            elif response == 'lefts':
                left()
                
            elif response == 'rights':
                right()

            elif response == 'nokeys':
                straight()

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


model = np.load(f'models/new_model-special.npy', allow_pickle=True).item()

# for key in ['straights', 'lefts', 'rights', 'nokeys']:
#     print(np.sum(model[key]['weights']))

main()
