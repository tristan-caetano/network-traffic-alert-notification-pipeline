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

from cgi import test
from gc import callbacks
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
import os

#  ---------------  Start of Algorithm  ---------------

# This function builds thd model.
def build_model():

    # # Set random seed
    # tf.random.set_seed(42)

    activationm = "softmax"
    # 1. Create the model (same as model_1 but with an extra layer)
    model_2 = tf.keras.Sequential([
        
        tf.keras.layers.Dense(7, input_shape = (7,), activation=activationm),
        tf.keras.layers.Dense(10, activation=activationm),
        tf.keras.layers.Dense(100, activation=activationm),        
        tf.keras.layers.Dense(1000, activation=activationm), 
        tf.keras.layers.Dense(100, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm),
        tf.keras.layers.Dense(6, activation="softmax") # output shape is 10, activation is softmax

        # tf.keras.layers.Conv1D(7, input_shape = (7,), kernel_size = (2), activation='relu'),
        # tf.keras.layers.MaxPooling1D((2)),
        # tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        # tf.keras.layers.MaxPooling1D((2)),
        # tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        # tf.keras.layers.MaxPooling1D((2)),
        # tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        # tf.keras.layers.MaxPooling1D((2)),
        # tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        # tf.keras.layers.MaxPooling1D((2)),
        # tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        # tf.keras.layers.MaxPooling1D((2)),

        # tf.keras.layers.Flatten(),
    
        # tf.keras.layers.Dense(64, activation='relu'),
        # tf.keras.layers.Dense(10, activation='softmax')
    ])

    # 2. Compile the model
    model_2.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=tf.keras.optimizers.SGD(learning_rate = .01), metrics=['accuracy'])
    return model_2


# This function will determine the types of malware packages. 
def determine_mal_packets(training_set, validation_set, testing_set):
    
    # Reads the CSV file.
    p_dataset = pd.read_csv(training_set, low_memory=False)
    v_p_dataset = pd.read_csv(validation_set, low_memory=False)
    test_p_dataset = pd.read_csv(testing_set, low_memory=False)

    #tf.shape(p_dataset)
    # p_dataset = np.asarray(p_dataset).astype('float32')
    # v_p_dataset = np.asarray(v_p_dataset).astype('float32')
    # test_p_dataset = np.asarray(test_p_dataset).astype('float32')

    # Saving binary classification column to variable.
    class_df = p_dataset['malname']
    vclass_df = v_p_dataset['malname']

    print(class_df)

    # Removing classifications from testing dataset.
    p_dataset = p_dataset.drop(['malname','ismal'], axis=1)
    v_p_dataset = v_p_dataset.drop(['malname','ismal'], axis=1)
    test_p_dataset = test_p_dataset.drop(['malname','ismal'], axis=1)

    # p_reshape = tf.reshape(p_dataset, [2,20,2,10])
    # v_p_reshape = tf.reshape(v_p_dataset, [2,20,2,10])
    # test_reshape = tf.reshape(test_p_dataset, [2,20,2,10])

    print(p_dataset.shape)
    # p_dataset = p_dataset.drop(['16'], axis=1)

    model_2 = build_model()
    
    # Create the learning rate callback
    lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-3 * 10**(epoch/20)) 
    
    model_2.fit(p_dataset, class_df, epochs=50, validation_data=(v_p_dataset, vclass_df))

    # Printing the model summary.
    # model_2.summary()

    #  ---------------  Saved Model  ---------------

    # Will save the entire model to a HDF5 file.
    # The '.h5' extension indicates that the model should be saved to HDF5.
    model_2.save('my_model.h5')

def saved_weights():

    # Recreate the exact same model, including its weights and the optimizer
    new_model = tf.keras.models.load_model('my_model.h5')

    # Prints the new model summary.
    new_model.summary()
    # Summary isn't diffrent from thw model_2.summary()

    #  ---------------  Saved Model  ---------------


    # Helps try to make an prediction
    output = new_model.predict("p_testing.csv")

    with open('predictions.txt','w') as notepad1:
        print(*output, file=notepad1, sep='\n')


# Calling function to test.
# CSV files created from train_test_creator then normalized. 
determine_mal_packets("p_training.csv", "p_validation.csv", "p_testing.csv")
# saved_weights()