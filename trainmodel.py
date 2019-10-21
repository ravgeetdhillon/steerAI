from variables import SCREEN_GRAB_EFFECTIVE_WIDTH, SCREEN_GRAB_EFFECTIVE_HEIGHT, RESIZE_FACTOR
from keys import w, a, d, nk
from datetime import datetime
from screen import show_image, convert_image
import numpy as np
import pandas as pd
from collections import Counter
import os
import random
import time
import cv2

# scaled_width = int( SCREEN_GRAB_EFFECTIVE_WIDTH * RESIZE_FACTOR )
# scaled_height = int( SCREEN_GRAB_EFFECTIVE_HEIGHT * RESIZE_FACTOR )

# size = int( scaled_width * (scaled_height * 17) / 30 )

size = 80*200

model = {
    'iterations': 0,
    'lefts': {
        'weights': np.zeros(size),
        'count': 0,
    },
    'rights': {
        'weights': np.zeros(size),
        'count': 0,
    },
    'straights': {
        'weights': np.zeros(size),
        'count': 0,
    },
    'nokeys': {
        'weights': np.zeros(size),
        'count': 0,
    },
}

part = 'part1'
accuracy_matrix = []
x = 1
for f in os.listdir(f'data/raw_dataset/{part}'):

    if f.split('-')[1].split('.')[0] in ['10','11','12','13']:
        continue
    
    if x == 10:
        break
    x += 1
    
    print(f'LOADING IMAGES... from {f}')
    
    train_images = np.load(f'data/raw_dataset/{part}/{f}', allow_pickle=True)

    np.random.shuffle(train_images)
    
    last = time.time()
    for count, img_data in enumerate(train_images):
        
        print(f'PART: {part} | FILE: {f} | NO.: {count + 1}')
        print(time.time() - last)
        print('-----')
        last = time.time()

        image = img_data[0]
        action = img_data[1]

        if action == w:
            action = 'straights'
            model[action]['count'] += 1
        elif action == a:
            action = 'lefts'
            model[action]['count'] += 1
        elif action == d:
            action = 'rights'
            model[action]['count'] += 1
        elif action == nk:
            action = 'nokeys'
            model[action]['count'] += 1

        image = convert_image(image)

        image = np.ndarray.flatten(image)

        for index, pixel in enumerate(image):
            if pixel == 255:
                model[action]['weights'][index] += 1

        model['iterations'] += 1

    for key in ['straights', 'lefts', 'rights', 'nokeys']:
        model[key]['weights'] /= model['iterations']


    test_choice = random.choice([10,11,12,13])
    test_images = np.load(f'data/raw_dataset/{part}/training_data-{test_choice}.npy', allow_pickle=True)
    
    accurate = 0
    for img_data in test_images:
        
        image = img_data[0]
        action = img_data[1]

        if action == w:
            action = 'straights'
        elif action == a:
            action = 'lefts'
        elif action == d:
            action = 'rights'
        elif action == nk:
            action = 'nokeys'

        image = convert_image(image)

        image = np.ndarray.flatten(image)

        image[image <= 128] = 0
        image[image > 128] = 1

        weightage = {
            'lefts': 0,
            'rights': 0,
            'straights': 0,
            'nokeys': 0,
        }

        for key in ['straights', 'lefts', 'rights', 'nokeys']:
            weightage[key] = np.sum( model[key]['weights'] * image )

        predicted_action = max(weightage.keys(), key=(lambda key: weightage[key]))

        print(predicted_action, action)

        if (action == 'straights' and predicted_action == 'nokeys') or (action == 'nokeys' and predicted_action == 'straights'):
            accurate += 1
        elif action == predicted_action:
            accurate += 1
        
    accuracy_matrix.append(accurate * 100 / len(test_images))
    print(f'Total: {len(test_images)} | Accuracy: {accurate * 100 / len(test_images)}')


    dt = '-'.join(datetime.now().isoformat().split('.')[0].split(':'))
    np.save(f'models/new_model-{dt}.npy', model)

    print('SAVED')

    print(accuracy_matrix)

    for key in ['straights', 'lefts', 'rights', 'nokeys']:
        model[key]['weights'] *= model['iterations']



# for key in ['straights', 'lefts', 'rights', 'nokeys']:
#     model[key]['weights'] /= model['iterations']

# time = '-'.join(datetime.now().isoformat().split('.')[0].split(':'))
# np.save(f'models/new_model-{time}.npy', model)

# print('SAVED')

# print(accuracy_matrix)
W