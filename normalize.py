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

    # Creating dataset from CSV data
    dataframe = pd.DataFrame(p_dataset)
    datalist = dataframe.values.tolist() # this MIGHT work, did not get to test because VScode broken

    # Normalize CSV
    gp.print(output, '\nNormalizing dataset, please wait.')

    #for x in datalist:
        #normalizedlist = preprocessing.normalize(datalist[x])  <-- need to make list for normalized values to be stored in, then make csv file from normalized values
                                                                # used this as resource for normalization https://www.educative.io/edpresso/data-normalization-in-python



    # Create tensor from csv data (NOT YET! this script is just for normalizing right now, use this code either after normalizing or in another script)
    # tensor = tf.constant([
    #     [[1,2,3],[4,5,6]],
    #     [[7,8,9],[10,11,12]],
    #     [[13,14,15], [16,17,18]]])
    # print(tensor)
    # print(tensor.ndim)