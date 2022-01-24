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


def determine_mal_packets(dataset):
    # Converting dataset to dataframe
    p_dataset = pd.read_csv(dataset, low_memory=False)

    # Saving binary classification column to variable
    class_df = p_dataset[p_dataset.columns[16]]

    # Removing classification from testing dataset
    p_dataset = p_dataset.drop(['1.3'], axis=1)

    # Set random seed
    tf.random.set_seed(42)

    # 1. Create the model (same as model_1 but with an extra layer)
    model_2 = tf.keras.Sequential([
        tf.keras.layers.Dense(1000),  # add an extra layer
        tf.keras.layers.Dense(100),
        tf.keras.layers.Dense(10),
        tf.keras.layers.Dense(1)
    ])

    # 2. Compile the model
    model_2.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                    optimizer=tf.keras.optimizers.Adam(),
                    metrics=['accuracy'])

    # 3. Fit the model
    model_2.fit(p_dataset, class_df, epochs=100, verbose=0)  # set verbose=0 to make the output print less
    model_2.evaluate(p_dataset, class_df)

    print(model_2.predict(p_dataset))

    # Printing model summary
    model_2.summary()
  
# Calling func for testing
determine_mal_packets("n_p_dataset.csv")
