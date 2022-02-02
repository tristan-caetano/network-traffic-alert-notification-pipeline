# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Creates a truncated test set for eventual AI algorithm

#  ---------------  Libraries  ---------------
import csv
import tkinter as tk
import numpy as np
import pandas as pd
import xlwt 
from pandas.core.arrays.sparse import dtype
from xlwt import Workbook
import GUI_print as gp

# Creating file that contains all the row number mal packets from the UNSW-NB15_1M.csv dataset 
# THIS SHOULD ONLY HAVE TO BE RUN ONCE PER FILE
def digest_file(dataset, output):
    
    # print('\nOpening original dataset, please wait.')
    gp.print(output, '\nOpening original dataset, please wait.')

    # Pandas Import CSV
    p_dataset = pd.read_csv(dataset, low_memory=False)

    # Creating dataset from CSV data
    dataframe = pd.DataFrame(p_dataset)
    col_name = []

    # Creating list of column names
    for col in dataframe:
        col_name.append(dataframe[col])

    # These arrays will contain the number of each malware type and each row that contains a malicious packet respectively
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    usable_rows = []
    mloc = 10

    # Prints number and names of unique values in malicious packet index
    unique_names = p_dataset[p_dataset.columns[mloc]].unique()

    # Creating a null value for the comparison
    null = p_dataset[p_dataset.columns[mloc]][0]

    gp.print(output, '\nIterating through entire dataset, this may take a bit.')

    # For loops that populate the respective arrays
    for x in range(len(p_dataset.index)):
        for y in range(len(unique_names)):
            if p_dataset[p_dataset.columns[mloc]][x] == unique_names[y] and p_dataset[p_dataset.columns[mloc]][x] != null:
                arr[y] += 1
                usable_rows.append(x)

    # Writing the rows numbers to a file to avoid sifting through the entire dataset repeatedly
    f = open('list_of_rows.txt', 'w')
    for rows in usable_rows:
        f.write(str(rows) + "\n")
    f.close()

    return(make_test_file(dataset, output, mloc))

# Creating CSV test set for Multilayer Perceptron
def make_test_file(dataset, output, mloc):

    # Max amount of packets per malicious type for test set
    maxMalAmt = 500

    # Name of output file
    test_set_file = 'perceptron_test_set.xls'

    # Opening original test set for data extraction
    r = open('list_of_rows.txt', 'r')

    max_col = 12

    # Taking idicies of malicious packets from text file and placing them in a list variable
    line = r.readlines()
    new_line = []
    for rows in line:
        temp = rows.strip().split('\n')
        temp = str(temp).strip("['']")
        new_line.append(int(temp))

    #print('\nOpening original dataset, please wait.')
    gp.print(output, '\nOpening original dataset, please wait.')

    # Pandas Import Original CSV
    p_dataset = pd.read_csv(dataset, low_memory = False)

    # Prints number and names of unique values in malicious packet index
    unique_names = p_dataset[p_dataset.columns[mloc]].unique()
 
    # Creating workbook to save test set until its written to a csv
    wb = Workbook() 
    sheet1 = wb.add_sheet('Sheet 1') 

    # Declaring variables for trackig packet count and tracking written rows
    counter = 0
    a = 0
    b = 0
    str_type = -1

    gp.print(output, '\nSaving list of malware packets, please wait.')

    # For loop that gets at most 50 of each type of malware and saves it to a spreadsheet
    for y in range(len(unique_names) - 1):
        counter = 0
        
        for x in range(len(new_line)):
            b = 0
            str_type = 0
            if p_dataset[p_dataset.columns[mloc]][new_line[x]] == unique_names[y+1] and counter < maxMalAmt:

                for z in range(max_col):
                    str_type = 0
                    temp_val = p_dataset[p_dataset.columns[z]][new_line[x]]
                    
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

                    elif z == 4 or z == 10: #or z == 5 or z == 13 or z == 47:
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
                counter += 1
                        
            elif(counter > maxMalAmt - 1):
                break

    # Resetting Counter so the next loop is not skipped
    counter = 0

    #print('\nSaving list of clean packets, please wait.')

    gp.print(output, '\nSaving list of clean packets, please wait.')

    # For loop that gets at most 1000 clean packets and saves to spreadsheet
    for x in range(len(p_dataset.index)):
        b = 0
        str_type = 0
        if int(p_dataset[p_dataset.columns[max_col - 1]][x]) == 0 and counter < 1000:
            
            for z in range(max_col):
                str_type = 0
                temp_val = p_dataset[p_dataset.columns[z]][x]
                print(int(z)) 
                    
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
                elif z == 4 or z == 10: #or z == 5 or z == 13 or z == 47:
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
            counter += 1

        elif(counter > 999):
            break

    # Create new XLS and save values to it
    wb.save(test_set_file)

    gp.print(output, '\nFile Created: perceptron_test_set.xls\nConverting XLS to CSV')
    
    # Converting XLS to CSV
    read_file = pd.read_excel (r'perceptron_test_set.xls', sheet_name='Sheet 1')
    read_file.to_csv (r'perceptron_test_set.csv', index = None, header=True)

    gp.print(output, ('\nFile Created: perceptron_test_set.csv'))

    return "perceptron_test_set.csv"

# Test Execution
#digest_file()
#make_test_file()