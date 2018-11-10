import numpy as np
import matplotlib.pyplot as plt
import random

from keras.datasets import mnist # CHANGE
from keras.models import Sequential

from keras.layers.core import Dense, Dropout, Activation
from keras.utils import np_utils

# Loading the training data
(X_train, y_train), (X_test, y_test) = mnist.load_data() # CHANGE

# Formatting the input data layer
X_train = X_train.reshape(60000, 784) # CHANGE DIMENSION
X_test = X_test.reshape(10000, 784) # CHANGE DIMENSION

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255 # CHANGE
X_test /= 255 # CHANGE

nb_classes = 10 # CHANGE OUTPUTS

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

# Building the 3-layer FCN
model = Sequential()
# First hidden layer
model.add(Dense(512, input_shape=(784,))) # CHANGE DIMENSION
model.add(Activation('relu'))
model.add(Dropout(0.2))
# Second hidden layer
model.add(Dense(512))   # CHANGE DIMENSION
model.add(Activation('relu'))
model.add(Dropout(0.2))
# Third Layer
model.add(Dense(10))
model.add(Activation('softmax'))
model.summary()

# Training the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train,Y_train,batch_size=128,epochs=5,verbose=1)
score = model.evaluate(X_test, Y_test)
print('Test score:', score[0])
print('Test accuracy:', score[1])

