# Network Traffic Alert Notification Pipeline Project
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Project Coordinator: Vinicius Coelho
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Algorithm that can determine malicious packets

#  ---------------  Libraries  ---------------

import tensorflow as tf
import pandas as pd
import numpy as np
import GUI

#  ---------------  Start of Algorithm  ---------------

# This function builds the model.
def build_model():

    multi = False

    # Changing activation
    activationm = "softmax"

    layers = 0

    if multi: layers = 6 
    else: layers = 1

    # Creating our model with Dense layers
    model_2 = tf.keras.Sequential([
        
        # Input Layer (7 Columns)
        tf.keras.layers.Dense(18, input_shape = (16,), activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 
        tf.keras.layers.Dense(10, activation=activationm), 

        # Output Layer (6 classes)
        tf.keras.layers.Dense(layers, activation="softmax") # output shape is 10, activation is softmax
    ])

    # Compiling the model
    if multi:
        model_2.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=tf.keras.optimizers.SGD(learning_rate = .0001), metrics=['accuracy'])
    else:
        model_2.compile(loss=tf.keras.losses.BinaryCrossentropy(), optimizer=tf.keras.optimizers.Adam(learning_rate = .0001), metrics=['accuracy'])
    
    return model_2

# This function will determine the types of malware packets. 
def determine_mal_packets(training_set, validation_set, testing_set):
    
    # Reads the CSV files.
    p_dataset = pd.read_csv(training_set, low_memory=False)
    v_p_dataset = pd.read_csv(validation_set, low_memory=False)
    test_p_dataset = pd.read_csv(testing_set, low_memory=False)

    # Saving multiclass classification column to variable.
    # class_df = p_dataset['malname']
    # vclass_df = v_p_dataset['malname']

    # Saving binary classification column to variable.
    class_df = p_dataset['ismal']
    vclass_df = v_p_dataset['ismal']

    # Removing classifications from testing datasets.
    p_dataset = p_dataset.drop(['malname','ismal'], axis=1)
    v_p_dataset = v_p_dataset.drop(['malname','ismal'], axis=1)
    test_p_dataset = test_p_dataset.drop(['malname','ismal'], axis=1)

    # Saving the built model to this variable
    model_2 = build_model()
    
    # Create the learning rate callback (not used)
    #lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-3 * 10**(epoch/20)) 

    # Fitting the model using the training and validation data
    model_2.fit(p_dataset, class_df, epochs=50, validation_data=(v_p_dataset, vclass_df))

    # Printing model summary
    model_2.summary()

    #  ---------------  Saved Model  ---------------

    # Will save the entire model to a HDF5 file.
    # The '.h5' extension indicates that the model should be saved to HDF5.
    model_2.save('curr_model.h5')

# This function takes in the testing data or converted set and saved model to make predictions
# Outputs the input CSV set with additional column containing predictions
def saved_weights(converted_set, model, gui_self):

    # Recreate the exact same model, including its weights and the optimizer
    GUI.SettingsWindow.updateMessage(gui_self, 30, "Loading model weights")
    new_model = tf.keras.models.load_model(model)

    # Taking in the data as a dataframe
    #test = pd.read_csv(converted_set, low_memory=False, encoding= "utf-8")
    GUI.SettingsWindow.updateMessage(gui_self, 40, "Loading converted set into algorithm")
    test = pd.read_csv(converted_set, low_memory=False, encoding= "utf-16")
    test.columns = [
                "srcport",      # 2
                "dstport",      # 4
                "timerel",      # 7
                "srctranbytes", # 8
                "dsttranbytes", # 9
                "timetolive",   # 10
                "dsttosrc",     # 18
                "srcwindow",    # 19
                "dstwindow",    # 20
                "srctcp",       # 21
                "dstseq",       # 22
                "srcmean",      # 23
                "setupround",   # 33
                "setupsynack",  # 34
                "setupackack",  # 35
                "ifequal",      # 36
                "malname",      # 48 
                "ismal" ]       # 49

    # Dropping binary and multiclass classification columns for testing set
    #test = test.drop(['malname','ismal'], axis=1)
    
    # Saving predictions to a variable
    GUI.SettingsWindow.updateMessage(gui_self, 50, "Making predictions on converted set")
    test_predictions = new_model.predict(test)

    # Taking the predictions and adding them to a new column labeled "predictions" in the input dataset
    GUI.SettingsWindow.updateMessage(gui_self, 75, "Saving predictions to file")
    get_test = np.argmax(test_predictions, axis = 1)
    test['predictions'] = get_test
    outfile = "predicted_" + converted_set

    # Saving the dataframe containing the predictions to a csv
    test.to_csv(outfile, index=True)

    GUI.SettingsWindow.updateMessage(gui_self, 90, "Sending predicted set to be displayed")
    return outfile

# Calling function to test.
# CSV files created from train_test_creator then parameterized. 
determine_mal_packets("p_training.csv", "p_validation.csv", "p_testing.csv")
# saved_weights("p_testing.csv", 'curr_model.h5')