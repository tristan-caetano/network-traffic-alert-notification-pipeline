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
import parameterize_mal as pmal
import GUI

#  ---------------  Start of Algorithm  ---------------
# This function builds the model.
def build_model(multi):

    # Changing activation
    activationm = "softmax"

    # Initializing layers variable
    layers = 0

    # Setting layer count based on the type of algorithm
    if multi: layers = 6 
    else: layers = 1

    # Creating our model with Dense layers
    model_2 = tf.keras.Sequential([
        
        # Input Layer (5 Columns) using softmax
        tf.keras.layers.Dense(5, input_shape = (5,), activation=activationm), 

        # 10 hidden layers with 10 neurons using softmax
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

        # Output Layer Multi(6 classes), Binary(1 class)  softmax activation
        tf.keras.layers.Dense(layers, activation="softmax") # output shape is 10, activation is softmax
    ])

    # Compiling the model based on the type of algorithm
    if multi:
        model_2.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=tf.keras.optimizers.SGD(learning_rate = .001), metrics=['accuracy'])
    else:
        model_2.compile(loss=tf.keras.losses.BinaryCrossentropy(), optimizer=tf.keras.optimizers.SGD(learning_rate = .001), metrics=['accuracy'])
    
    return model_2

# This function will determine the types of malware packets. 
def determine_mal_packets(training_set, validation_set, testing_set, multi, output_model_name):
    
    # Reads the CSV files.
    p_dataset = pd.read_csv(training_set, low_memory=False)
    v_p_dataset = pd.read_csv(validation_set, low_memory=False)
    test_p_dataset = pd.read_csv(testing_set, low_memory=False)

    # Setting class column depending on the algorithm type
    if multi:
        # Saving multiclass classification column to variable.
        class_df = p_dataset['malname']
        vclass_df = v_p_dataset['malname']
    else:
        # Saving binary classification column to variable.
        class_df = p_dataset['ismal']
        vclass_df = v_p_dataset['ismal']

    # Removing classifications from testing datasets.
    p_dataset = p_dataset.drop(['malname','ismal'], axis=1)
    v_p_dataset = v_p_dataset.drop(['malname','ismal'], axis=1)
    test_p_dataset = test_p_dataset.drop(['malname','ismal'], axis=1)

    # Saving the built model to this variable
    model_2 = build_model(multi)
    
    # Create the learning rate callback (not used)
    #lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-3 * 10**(epoch/20)) 

    # Fitting the model using the training and validation data
    model_2.fit(p_dataset, class_df, epochs=50, validation_data=(v_p_dataset, vclass_df))

    # Printing model summary
    model_2.summary()

    #  ---------------  Saved Model  ---------------

    # Will save the entire model to a HDF5 file.
    # The '.h5' extension indicates that the model should be saved to HDF5.
    model_2.save(output_model_name)

# This function takes in the testing data or converted set and saved model to make predictions
# Outputs the input CSV set with additional column containing predictions
def saved_weights(converted_set, non_norm_set, model, gui_self):

    # Recreate the exact same model, including its weights and the optimizer
    GUI.SettingsWindow.updateMessage(gui_self, 50, "Loading model weights")
    new_model = tf.keras.models.load_model(model)

    # Taking in the data as a dataframe
    #test = pd.read_csv(converted_set, low_memory=False, encoding= "utf-8")
    GUI.SettingsWindow.updateMessage(gui_self, 60, "Loading converted set into algorithm")

    # Try except for the encoding on the input file
    try:
        test = pd.read_csv(converted_set, low_memory=False, encoding= "utf-8")
    except:
        test = pd.read_csv(converted_set, low_memory=False, encoding= "utf-16")

    # Try except for the non normalized file
    try:
        n_norm = pd.read_csv(non_norm_set, low_memory=False, encoding= "utf-8")
    except:
        n_norm = pd.read_csv(non_norm_set, low_memory=False, encoding= "utf-16")

    # Dropping binary and multiclass classification columns for testing set (Not used in main pipeline)
    #test = test.drop(['malname','ismal'], axis=1)
    
    # Saving predictions to a variable
    GUI.SettingsWindow.updateMessage(gui_self, 70, "Making predictions on converted set")
    test_predictions = new_model.predict(test)

    # Taking the predictions and adding them to a new column labeled "predictions" in the input dataset
    GUI.SettingsWindow.updateMessage(gui_self, 80, "Saving predictions to file")
    get_test = np.argmax(test_predictions, axis = 1)
    n_norm['predictions'] = get_test

    # Filling null values with 0
    n_norm.fillna(value = 0, inplace = True)

    # Creating name for outfile
    outfile = "predicted_" + non_norm_set

    # Saving the dataframe containing the predictions to a csv
    n_norm.to_csv(outfile, index=False)

    # Reversing parameterization
    pmal.rev_param(outfile)

    GUI.SettingsWindow.updateMessage(gui_self, 90, "Sending predicted set to be displayed")
    return outfile