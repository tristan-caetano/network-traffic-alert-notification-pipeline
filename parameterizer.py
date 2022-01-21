# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Changes selected string values in dataset to integers, can be expanded easily

#  ---------------  Libraries  ---------------
import tkinter as tk
import numpy as np
import pandas as pd
import xlwt 
from pandas.core.arrays.sparse import dtype
from xlwt import Workbook
import GUI_print as gp

# Creating CSV test set for Multilayer Perceptron
def parameterize(infile, output):

    # Name of output file
    test_set_file = 'p_converted.xls'

    max_col = 10

    #print('\nOpening original dataset, please wait.')
    gp.print(output, '\nOpening converted dataset, please wait.')

    # Pandas Import Original CSV
    p_dataset = pd.read_csv(infile, low_memory = False)
 
    # Creating workbook to save test set until its written to a csv
    wb = Workbook() 
    sheet1 = wb.add_sheet('Sheet 1') 

    # Declaring variables for tracking packet count and tracking written rows
    a = 0
    b = 0
    str_type = -1

    gp.print(output, '\nParameterizing dataset, please wait.')
        
    for x in range(len(p_dataset.index)):
        b = 0
        str_type = 0
        #for z in range(49):
        for z in range(max_col):
            str_type = 0
            temp_val = p_dataset[p_dataset.columns[z]][x]
            
            if z == 0 or z == 2:
                str_type = 1
                try:
                    temp_val = temp_val.split('.')
                    for q in temp_val:
                        sheet1.write(a, b, str(q))
                        b += 1
                except AttributeError:
                    print("Incorrect IP format")
                    b += 4

            elif z == 4: #or z == 5 or z == 13 or z == 47:
                parameterize = p_dataset[p_dataset.columns[z]].unique()
                
                for w in parameterize:
                    if w == temp_val:
                        temp_val = np.where(parameterize == w)

                        # Removing remaining strings
                        temp_val = str(temp_val).replace("(", "")
                        temp_val = str(temp_val).replace(")", "")
                        temp_val = str(temp_val).replace("[", "")
                        temp_val = str(temp_val).replace("]", "")
                        temp_val = str(temp_val).replace(",", "")
                        temp_val = str(temp_val).replace("array", "")
            

            if str_type == 0:
                sheet1.write(a, b, str(temp_val))
                b += 1

        a += 1

    # Create new XLS and save values to it
    wb.save(test_set_file)

    gp.print(output, '\nFile successfully parameterized!\nFile Created: '+ test_set_file + '\nConverting XLS to CSV')
    
    # Converting XLS to CSV
    read_file = pd.read_excel (r'p_converted.xls', sheet_name='Sheet 1')
    read_file.to_csv (r'p_converted.csv', index = None, header=True)

    gp.print(output, ('\nFile Created: p_converted.csv'))

    return "p_converted.csv"