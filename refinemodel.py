from variables import SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT, RESIZE_FACTOR
from screen import show_image
import numpy as np


def refine_model(action_name):
    '''
    Refine the model for fast loading time.
    '''

    print(f'STARTING {action_name}')

    # load the model for the given action
    model = np.load(f'model/model-{action_name}.npy', allow_pickle=True).item()

    # create a master image which is the combination of maximum value for each pixel
    image = []

    width = int(SCREEN_GRAB_WIDTH * RESIZE_FACTOR)
    height = int(SCREEN_GRAB_HEIGHT * RESIZE_FACTOR * 2 // 3)
    
    for i in range(height):
        image.append([])

        for j in range(width):
            pixel = model.get(f'{i}, {j}')
            a = max(pixel.keys(), key=(lambda key: pixel[key]))
            image[-1].append(a)

    # save the refined model in the form of the numpy array of the image
    image = np.array(image, dtype='uint8')
    np.save(f'model/refined-model-{action_name}.npy', image)

    print(f'SAVED {action_name}')


def main():

    # init the process
    print('STARTING.')

    # refine the individual models
    refine_model('straights')
    refine_model('lefts')
    refine_model('rights')
    refine_model('nokeys')

    print('4 MODELS REFINED.')


main()
