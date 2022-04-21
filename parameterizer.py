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
# THIS FILE IS CURRENTLY NOT BEING USED WITHIN THE PIPELINE
# IT HAS BEEN REPLACED WITH parameterize_mal.py

#  ---------------  Libraries  ---------------
import numpy as np
import pandas as pd
import GUI
from pandas.core.arrays.sparse import dtype
from xlwt import Workbook

# Creating CSV test set for Multilayer Perceptron
def parameterize(infile, gui_self):

    # Name of output file
    test_set_file = 'p_converted.xls'

    max_col = 10

    GUI.SettingsWindow.updateMessage(gui_self, 30, "Reading converted file.")

    # Pandas Import Original CSV
    p_dataset = pd.read_csv(infile, low_memory = False, encoding= "utf-16")
    # p_dataset = p_dataset.rename(columns=[
    #             0: "srcip", 
    #             1: "srcport",
    #             2: "dstip",
    #             3: "dstport",
    #             4: "protocol",
    #             5: "timerel", 
    #             6: "tranbytes", 
    #             7: "timetolive", 
    #             8: "srctcp", 
    #             9: "dsttcp", 
    #             10: "malname", 
    #             11: "ismal"])
    # p_dataset = p_dataset.drop(["srcip", "dstip", "protocol"])
 
    # Creating workbook to save test set until its written to a csv
    wb = Workbook() 
    sheet1 = wb.add_sheet('Sheet 1') 

    # Declaring variables for tracking packet count and tracking written rows
    a = 0
    b = 0
    str_type = -1

    GUI.SettingsWindow.updateMessage(gui_self, 40, "Parameterizing values.")
        
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
    
    GUI.SettingsWindow.updateMessage(gui_self, 50, "Saving parameterized file.")

    # Converting XLS to CSV
    read_file = pd.read_excel (r'p_converted.xls', sheet_name='Sheet 1')
    read_file.to_csv (r'p_converted.csv', index = None, header=True)

    return "p_converted.csv"