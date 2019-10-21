from variables import BATCH_SIZE
from collections import Counter
# from keys import a, s, w, d, wa, wd, nk
from keys import a, w, d, nk
from random import shuffle
import numpy as np
import os
import math


def setup():
    '''
    Setup the project space for storing the training data.
    '''

    if not os.path.exists('data/dataset/final'):
        os.mkdir('data/dataset/final')

    starting_value = len(os.listdir('data/dataset/final')) + 1
    total_files = len(os.listdir('data/dataset/part1'))

    return (starting_value, total_files)


def balance_data(images):
    '''
    Balance the data for a good model.
    '''

    straights = []
    lefts = []
    rights = []
    nokeys = []

    # shuffle the images to create some randomness
    shuffle(images)

    # divide data based on the actions
    for image in images:
        if image[1] == w:
            straights.append(image)
        elif image[1] == a:
            lefts.append(image)
        elif image[1] == d:
            rights.append(image)
        elif image[1] == nk:
            nokeys.append(image)

    # find the action with least amount
    # this will be our balancing point
    balance = min(len(straights), len(lefts),
                  len(rights), len(nokeys))
    
    straights = straights[:balance]
    lefts = lefts[:balance]
    rights = rights[:balance]
    nokeys = nokeys[:balance]

    return (straights, lefts, rights, nokeys)


def main():

    starting_value, total_files = setup()
    print(f'STARTING WITH VALUE : {starting_value}')

    # process the dataset in batches for performance and memory gains
    for batch in range(0, math.ceil(total_files / BATCH_SIZE)):

        print(f'STARTING BATCH: {batch}')

        batch_start = (batch * BATCH_SIZE) + 1
        master = {
            'straights': [],
            'lefts': [],
            'rights': [],
            'nokeys': [],
        }

        # load the files one by one from each data set during a batch
        for i in range(batch_start, batch_start + BATCH_SIZE):

            try:
                images = np.load(
                    f'data/dataset/part1/training_data-{i}.npy', allow_pickle=True)

                # get the balanced data
                straights, lefts, rights, nokeys = balance_data(images)

                # append the returned balanced data to a master dictionary
                master['straights'] += straights
                master['lefts'] += lefts
                master['rights'] += rights
                master['nokeys'] += nokeys
                
                print(f'---FILE ID {i}')

            except:
                break

        np.save(
            f'data/dataset/final/final_training_data-{starting_value}.npy', master)
        starting_value += 1
        print('SAVED')


main()
