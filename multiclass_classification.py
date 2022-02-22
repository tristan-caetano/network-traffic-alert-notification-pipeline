# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Artificial Intelligence algorithm that can determine malicious packets

#  ---------------  Libraries  ---------------

# garbage collection library?? 
from gc import callbacks

import tensorflow as tf
from tensorflow import keras

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


#  ---------------  Start of Algorithm  ---------------

# This function builds thd model.
def build_model():

    # Set random seed
    tf.random.set_seed(42)

    # 1. Create the model (same as model_1 but with an extra layer)
    model_2 = tf.keras.Sequential([
        # tf.keras.layers.Dense(1000, activation=None),  # add an extra layer
        # tf.keras.layers.Dense(100),
        # tf.keras.layers.Dense(10),
        # tf.keras.layers.Dense(1)
        
        tf.keras.layers.Dense(10, input_dim = 8, activation="relu"),
        tf.keras.layers.Dense(10, activation="relu"),
        tf.keras.layers.Dense(10, activation="relu"),
        tf.keras.layers.Dense(9, activation="softmax") # output shape is 10, activation is softmax
    ])

    # 2. Compile the model
    model_2.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=tf.keras.optimizers.Adam(learning_rate = .001), metrics=['accuracy'])
    return model_2


# This function will determine the types of malware packages. 
def determine_mal_packets(dataset):
    
    # Reads the CSV file.
    p_dataset = pd.read_csv(dataset, low_memory=False)

    # Saving binary classification column to variable.
    class_df = p_dataset['16']
    # print(class_df)

    # Removing classifications from testing dataset.
    p_dataset = p_dataset.drop(['0','1','2','3','5','6','7','8','16','17'], axis=1)
    # p_dataset = p_dataset.drop(['16'], axis=1)

    model_2 = build_model()
    
    # Create the learning rate callback
    lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-3 * 10**(epoch/20))
    
    model_2.fit(p_dataset, class_df, epochs=100, validation_data=(p_dataset, class_df), callbacks = lr_scheduler)

    # Printing the model summary.
    # model_2.summary()

    #  ---------------  Saved Model  ---------------

    # Will save the entire model to a HDF5 file.
    # The '.h5' extension indicates that the model should be saved to HDF5.
    model_2.save('my_model.h5')

    # Recreate the exact same model, including its weights and the optimizer
    new_model = tf.keras.models.load_model('my_model.h5')

    # Prints the new model summary.
    new_model.summary()
    # Summary isn't diffrent from thw model_2.summary()

    #  ---------------  Saved Model  ---------------


# Helps try to make an prediction
    # model_2.predict()

# Calling function to test.
determine_mal_packets("n_p_dataset.csv")
