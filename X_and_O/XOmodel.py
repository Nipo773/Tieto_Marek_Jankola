import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout, Activation
from keras.layers import Conv2D, MaxPooling2D
from PIL import Image

def train():
    

    train_X, train_y = load_data()

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(28, 28, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    model.fit(train_X, train_y, epochs=8, batch_size=32)

    return model

def load_data():
    data = np.array([])
    for i in range(7,3652):
        image = np.array(Image.open("XOtrain/" + str(i) + ".jpg").resize((28,28)))
        data = np.append(data, image)

    data = data.reshape(3645, 28, 28, 3)
    data_X = np.concatenate((data[0:123], data[246:1640], data[2050:2091], data[2501:2542], data[2952:2993], data[3403:3444]))
    data_O = np.concatenate((data[123:246], data[1640:2050], data[2091:2501], data[2542:2952], data[2993:3403], data[3444:]))

    data_train_y = np.array([1 for i in range(len(data_X[:1500]))] + [0 for i in range(len(data_O[:1500]))])
    data_train_X = np.concatenate((data_X[:1500], data_O[:1500]))
    data_train_y = to_categorical(data_train_y)

    return data_train_X, data_train_y
    
