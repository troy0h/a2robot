import tensorflow  as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

# Create a classifier object os Sequential class
train_Dgen = ImageDataGenerator(rescale = 1./255,
shear_range = 0.2,
zoom_range = 0.2,
horizontal_flip = True)

test_Dgen = ImageDataGenerator(rescale = 1./255)
training_set = train_Dgen.flow_from_directory('resource/train',
target_size = (320, 180),
batch_size = 15,
class_mode = 'categorical')

test_set = test_Dgen.flow_from_directory('resource/test',
target_size = (320, 180),
batch_size = 15,
class_mode = 'categorical')

model = Sequential()

# Add Layers
model.add(Conv2D(32, (3, 3), input_shape = (320, 180, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (3, 3)))
model.add(Flatten())
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 3, activation = 'sigmoid'))

# Compile the modfel
model.compile(optimizer = 'adam', 
              loss = 'categorical_crossentropy', 
              metrics = ['accuracy'])

# Fit the data to the model
validation_steps = len(test_set)
model.fit(training_set,epochs = 20,
validation_data = test_set)

# Save the model
model.save('resource/model.keras')
print('saved')