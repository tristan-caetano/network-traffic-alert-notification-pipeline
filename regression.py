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

import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def runConvertedSet(checkpoint):

    # Set random seed
    tf.random.set_seed(42)

    # 1. Create the model (same as model_1 but with an extra layer)
    model_2 = tf.keras.Sequential([
        tf.keras.layers.Dense(1000, activation=None),  # add an extra layer
        tf.keras.layers.Dense(100),
        tf.keras.layers.Dense(10),
        tf.keras.layers.Dense(1)
    ])

    # 2. Compile the model
    model_2.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
                    metrics=['accuracy'])

    model_2.built = True  

    model_2.load_weights(checkpoint)
    predictions = model_2.predict("n_p_converted.csv")
    print(predictions)



def determine_mal_packets(dataset):
    
    # Converting dataset to dataframe
    p_dataset = pd.read_csv(dataset, low_memory=False)

    # Saving binary classification column to variable
    class_df = p_dataset['7']
    print(class_df)

    # Removing classification from testing dataset
    p_dataset = p_dataset.drop(['7'], axis=1)
    # p_dataset = p_dataset.drop(['16'], axis=1)

    # Set random seed
    tf.random.set_seed(42)

    # 1. Create the model (same as model_1 but with an extra layer)
    model_2 = tf.keras.Sequential([
        tf.keras.layers.Dense(1000, activation=None),  # add an extra layer
        tf.keras.layers.Dense(100),
        tf.keras.layers.Dense(10),
        tf.keras.layers.Dense(1)
    ])

    # 2. Compile the model
    model_2.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                    optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
                    metrics=['accuracy'])

    # 3. Fit the model
    checkpoint_path = "training_2/cp-{epoch:04d}.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_dir, save_weights_only=True, verbose=1)

    model_2.fit(p_dataset, 
          class_df,  
          epochs=100,
          validation_data=(p_dataset, class_df),
          callbacks=[cp_callback])

    # model_2.fit(p_dataset, class_df, epochs=100, verbose=0)  # set verbose=0 to make the output print less
    #model_2.evaluate(p_dataset, class_df)

    # Printing model summary
    model_2.summary()

    # Helps try to make an prediction
    # model.predict()

    
  
# Calling func for testing
#determine_mal_packets("n_p_dataset.csv")
runConvertedSet("model.ckpt")
