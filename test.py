from variables import SCREEN_GRAB_START_WIDTH, SCREEN_GRAB_START_HEIGHT, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT, RESIZE_FACTOR, SAVE_POINT, RESIZE_FACTOR
from screen import show_image, convert_image, screenshot
# from keys import w, a, d, nk
import numpy as np
import os
# import sys
# from time import time
# import pandas as pd
# from collections import Counter
# from datetime import datetime
# import cv2

images = np.load(f'data/raw_dataset/part1/training_data-10.npy', allow_pickle=True)

# left = np.ndarray.flatten( convert_image( images[85][0] ) )
# right = np.ndarray.flatten( convert_image( images[156][0] ) )
# straight = np.ndarray.flatten( convert_image( images[255][0] ) )
# nokey = np.ndarray.flatten( convert_image( images[325][0] ) )


for i in range(400):
# i = 325
    image = images[i][0]
    # show_image(image)
    image = convert_image(image)
    show_image(image)

# model = {
#     'iterations': 1,
#     'lefts': {
#         'weights': left,
#         'count': 0,
#     },
#     'rights': {
#         'weights': right,
#         'count': 0,
#     },
#     'straights': {
#         'weights': straight,
#         'count': 0,
#     },
#     'nokeys': {
#         'weights': nokey,
#         'count': 0,
#     },
# }

# np.save(f'models/new_model-special.npy', model)


# f = 'training_data-9.npy'

# if f.split('-')[1].split('.')[0] in ['10','11','12','13']:
#     print(555)
# a = np.array( [154,23,189,78,2] )

# a[a <= 128] = 0
# a[a > 128] = 1


    # if output == a and len(lefts) < SAVE_POINT // 4:
    #                 lefts.append( [screen, output] )
    #             elif output == d and len(rights) < SAVE_POINT // 4:
    #                 rights.append( [screen, output] )
    #             elif output == w and len(straights) < SAVE_POINT // 4:
    #                 straights.append( [screen, output] )
    #             elif output == nk and len(nokeys) < SAVE_POINT // 4:
    #                 nokeys.append( [screen, output] )

# buffer = []

# print(buffer[-1])

# listChar = [
#     ['zz',[1,0]],
#     ['z',[1,0]],
#     ['zz',[1,0]],
# ]

# def are_equal(data):
    
#     if all(i[1] == data[0][1] for i in data):
#         return True
#     else:
#         return False

# image = screenshot(region=(SCREEN_GRAB_START_WIDTH, SCREEN_GRAB_START_HEIGHT, SCREEN_GRAB_WIDTH, SCREEN_GRAB_HEIGHT))
# show_image(image)
# image = convert_image(image)
# show_image(image)

# lefts = model['lefts']['weights']

# for key in ['straights', 'lefts', 'rights', 'nokeys']:
#     # print(np.sum( model[key]['weights'] ))
#     print(model[key]['count'] )
    
    # weightage[key] = np.sum( model[key]['weights'] * image )


# lefts = lefts.reshape(170, 400)

# show_image(lefts)

# print(np.max(lefts), lefts.shape)
# time = datetime.now().isoformat()
# time = '2019-10-18T17:48:38.038987'

# time = '-'.join(time.split('.')[0].split(':'))
# print(time)

# scaled_width = int( SCREEN_GRAB_EFFECTIVE_WIDTH * RESIZE_FACTOR )
# scaled_height = int( SCREEN_GRAB_EFFECTIVE_HEIGHT * RESIZE_FACTOR )

# size = int( scaled_width * (scaled_height * 17) / 30 )
# print(size)


# weightage = {
#     'lefts': 10,
#     'rights': 20,
#     'straights': 20,
#     'nokeys': 5,
# }

# a = max(weightage.keys(), key=(lambda key: weightage[key]))
# print(a)


# images = np.load(f'data/raw_dataset/part1/training_data-10.npy', allow_pickle=True)
# for i in range(400):
# i = 325
# image = images[i][0]
# show_image(image)
# image = convert_image(image)
# show_image(image)

# a = np.array([2,4,3.5])
# b = np.array([5,8,10])

# print(np.sum(a*b))

# df = pd.DataFrame(images)
# print(Counter(df[1].apply(str)))


# a = np.array([1] * 400 * 300)
# b = np.array([1] * 400 * 300)
# d = time()
# c = a * b

# print(time() - d)


# a = np.array([[4.2,5,5,1],
#              [4,5,5.1,1],
#              [4,5,5,1],
#              [4,5,5,1],
#              [4,5,5,1]])

# b = np.zeros(20)

# c = np.ndarray.flatten(a)

# d = (b+c) / 200000



# part = 'part2'
# print('LOADING IMAGES...')
# images = np.load(f'data/raw_dataset/{part}/training_data-1.npy', allow_pickle=True)
# test_images = images[:]

# np.random.shuffle(test_images)

# model = np.load(f'models/new_model-2019-10-21T16-08-04.npy', allow_pickle=True).item()

# image = model['lefts']['weights'].reshape(80, 200)
# image *= 255
# # iterations = model['iterations']
# # print(iterations)
# print(np.sum(image))
# # print(image)
# # print(list(image))

# show_image(image)

# print(model)

# accurate = 0
# for img_data in test_images:
#     image = img_data[0]
#     action = img_data[1]

#     if action == w:
#         action = 'straights'
#     elif action == a:
#         action = 'lefts'
#     elif action == d:
#         action = 'rights'
#     elif action == nk:
#         action = 'nokeys'

#     image = convert_image(image)

#     image = np.ndarray.flatten(image)

#     weightage = {
#         'lefts': 0,
#         'rights': 0,
#         'straights': 0,
#         'nokeys': 0,
#     }

#     for key in ['straights', 'lefts', 'rights', 'nokeys']:
#         weightage[key] = np.sum( model[key]['weights'] * image )

#     predicted_action = max(weightage.keys(), key=(lambda key: weightage[key]))

#     print(predicted_action, action)

#     if action == predicted_action:
#         accurate += 1
    
# print(f'Total: {len(test_images)} | Accuracy: {accurate * 100 / len(test_images)}')
