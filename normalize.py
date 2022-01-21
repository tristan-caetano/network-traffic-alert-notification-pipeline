# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Data Normalizer

#  ---------------  Libraries  ---------------
import tkinter as tk
import pandas as pd
import GUI_print as gp
from sklearn import preprocessing
import numpy as np
# import tensorflow as tf
# from tensorflow.python.ops.gen_array_ops import shape

# Creating CSV test set for Multilayer Perceptron
def digest_file(infile, output):

    gp.print(output, '\nOpening test set, please wait.')

    # Pandas Import CSV
    p_dataset = pd.read_csv(infile, low_memory=False)

    gp.print(output, '\nNormalizing dataset, please wait.')

    # Min Max Normalization
    t_df = p_dataset.values
    min_max_scaler = preprocessing.MinMaxScaler()
    t_df_scaled = min_max_scaler.fit_transform(t_df)
    n_df = pd.DataFrame(t_df_scaled)

    # Save new normalized CSV file
    n_df.to_csv("n_p_dataset.csv", index=False)

    # Returning name of csv file
    return "n_p_dataset.csv"