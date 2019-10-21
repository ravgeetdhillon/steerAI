import numpy as np
import os
import time
from screen import show_image
from random import shuffle

model = {
    'iterations': 0,
    'weights': 0,
}

def learn(action, action_name):
    
    size = len(action)
    
    print(f'CURRENT ACTION: {action_name}')

    for index, image in enumerate(action):
        rows, cols = image[0].shape
        image = image[0]

        last = time.time()

        for i in range(rows):
            for j in range(cols):
                if (f'{i}, {j}') not in model:
                    model[ f'{i}, {j}' ] = {}

                if image[i][j] not in model[ f'{i}, {j}' ]:
                    model[ f'{i}, {j}' ][ image[i][j] ] = 1
                else:
                    model[ f'{i}, {j}' ][ image[i][j] ] += 1

        
        print(f'COMPLETED: {(index + 1) * 100 / size}% TOTAL: {size} LEFT: {size - (index + 1)}')
        
        now = time.time()
        print(now - last)


    np.save(f'model/model-{action_name}.npy', model)
    print(f'SAVED: {action_name}')
    print('---------------------')


straights = []
lefts = []
rights = []
nokeys = []


for i in range(1, len(os.listdir('data/dataset/final')) + 1):
    
    images = np.load(f'data/dataset/final/final_training_data-{i}.npy', allow_pickle=True)

    straights += images.item()['straights']
    lefts += images.item()['lefts']
    rights += images.item()['rights']
    nokeys += images.item()['nokeys']

shuffle(straights)
shuffle(lefts)
shuffle(rights)
shuffle(nokeys)

straights = straights[:300]
lefts = lefts[:300]
rights = rights[:300]
nokeys = nokeys[:300]


learn(straights, 'straights')
learn(lefts, 'lefts')
learn(rights, 'rights')
learn(nokeys, 'nokeys')
