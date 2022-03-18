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
from cgi import test
from gc import callbacks
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import os


#  ---------------  Start of Algorithm  ---------------

# This function builds thd model.
def build_model():

    # Set random seed
    tf.random.set_seed(42)

    # 1. Create the model (same as model_1 but with an extra layer)
    model_2 = tf.keras.Sequential([
        
        tf.keras.layers.Dense(10, input_dim = 7, activation="relu"),
        # tf.keras.layers.Dense(9, activation="relu"),
        # tf.keras.layers.Dense(9, activation="relu"),
        # tf.keras.layers.Dense(9, activation="relu"),
        # tf.keras.layers.Dense(10, activation="softmax") # output shape is 10, activation is softmax

        tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        tf.keras.layers.MaxPooling1D((2)),
        tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        tf.keras.layers.MaxPooling1D((2)),
        tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        tf.keras.layers.MaxPooling1D((2)),
        tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        tf.keras.layers.MaxPooling1D((2)),
        tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        tf.keras.layers.MaxPooling1D((2)),
        tf.keras.layers.Conv1D(32, kernel_size = (2), activation='relu'),
        tf.keras.layers.MaxPooling1D((2)),

        tf.keras.layers.Flatten(),
    
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    # 2. Compile the model
    model_2.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=tf.keras.optimizers.SGD(learning_rate = .0001), metrics=['accuracy'])
    return model_2


# This function will determine the types of malware packages. 
def determine_mal_packets(training_set, validation_set, testing_set):
    
    # Reads the CSV file.
    p_dataset = pd.read_csv(training_set, low_memory=False)
    v_p_dataset = pd.read_csv(validation_set, low_memory=False)
    test_p_dataset = pd.read_csv(testing_set, low_memory=False)

    # Saving binary classification column to variable.
    class_df = p_dataset['7']
    print(class_df)
    vclass_df = v_p_dataset['7']
    print(v_p_dataset)
    # print(class_df)

    # Removing classifications from testing dataset.
    p_dataset = p_dataset.drop(['7','8'], axis=1)
    v_p_dataset = v_p_dataset.drop(['7','8'], axis=1)
    test_p_dataset = test_p_dataset.drop(['7','8'], axis=1)

    # p_reshape = tf.reshape(p_dataset, [2,20,2,10])
    # v_p_reshape = tf.reshape(v_p_dataset, [2,20,2,10])
    # test_reshape = tf.reshape(test_p_dataset, [2,20,2,10])

    print(p_dataset.shape)
    # p_dataset = p_dataset.drop(['16'], axis=1)

    model_2 = build_model()
    
    # Create the learning rate callback
    lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-3 * 10**(epoch/20))
    
    model_2.fit(p_dataset, class_df, epochs=100, validation_data=(v_p_dataset, vclass_df), callbacks = lr_scheduler)

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
    output = model_2.predict(test_p_dataset)

    with open('predictions.txt','w') as notepad1:
        print(*output, file=notepad1, sep='\n')


# Calling function to test.
# CSV files created from train_test_creator then normalized.
# determine_mal_packets("n_n_training.csv", "n_n_validation.csv", "n_n_testing.csv")
