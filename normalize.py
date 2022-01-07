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
import tensorflow as tf
from tensorflow.python.ops.gen_array_ops import shape

# Creating CSV test set for Multilayer Perceptron
def normalize(infile, output):
    gp.print(output, '\nNormalizing dataset, please wait.')

    # Pandas Import Original CSV
    p_dataset = pd.read_csv(infile, low_memory = False)




    #need to normalize csv here, remove periods in IPs etc...




    # Create tensor from csv data UNFINISHED
    tensor = tf.constant([
        [[1,2,3],[4,5,6]],
        [[7,8,9],[10,11,12]],
        [[13,14,15], [16,17,18]]])
    print(tensor)
    print(tensor.ndim)