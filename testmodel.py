import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from screen import get_data, show_image
import numpy as np
import sys


# load test images
data = get_data()
np.random.shuffle(data)
images = np.array( [d[0] for d in data] ) / 255
labels = np.array( [d[1] for d in data] )

div = 100
test_images = images[div:]
test_labels = labels[div:]


# load the model
model = tf.keras.models.load_model('sdc-cnn-model.h5')

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`

c = 0
for i in range( len(test_images) ):
    print(f'Current: {i}')
    image = test_images[i]
    label = test_labels[i]

    image = tf.cast(image, tf.float32)

    prediction = model.predict(np.array([image])).tolist()[0]
    choice = prediction.index( max(prediction) )
