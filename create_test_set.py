import csv
import pandas as pd
import xlwt 
from pandas.core.arrays.sparse import dtype
from xlwt import Workbook

# Creating file that contains all the row number mal packets from the UNSW-NB15_1.csv dataset 
# THIS SHOULD ONLY HAVE TO BE RUN ONCE PER FILE
def digest_file():
    
    print('\nOpening original dataset, please wait.')
    # Pandas Import CSV
    p_dataset = pd.read_csv('UNSW-NB15_1.csv', low_memory=False)

    # Creating dataset from CSV data
    dataframe = pd.DataFrame(p_dataset)

    # These arrays will contain the number of each malware type and each row that contains a malicious packet respectively
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    usable_rows = []

    # Prints number and names of unique values in malicious packet index
    #unique_vals = p_dataset[p_dataset.columns[47]].nunique()
    unique_names = p_dataset[p_dataset.columns[47]].unique()

    # Creating a null value for the comparison
    null = p_dataset[p_dataset.columns[47]][0]

    print('\nIterating through entire dataset, this may take a bit.')
    # For loops that populate the respective arrays
    for x in range(700000):
        for y in range(10):
            if p_dataset[p_dataset.columns[47]][x] == unique_names[y] and p_dataset[p_dataset.columns[47]][x] != null:
                arr[y] += 1
                usable_rows.append(x)

    # Writing the rows numbers to a file to avoid sifting through the entire dataset repeatedly
    f = open('list_of_rows.txt', 'w')
    for rows in usable_rows:
        f.write(str(rows) + "\n")
    f.close()

    print('\nFile Created: list_of_rows.txt')

    make_test_file()

# Creating CSV test set for Multilayer Perceptron
def make_test_file():

    # Opening original test set for data extraction
    r = open('list_of_rows.txt', 'r')

    # Taking idicies of malicious packets from text file and placing them in a list variable
    line = r.readlines()
    new_line = []
    for rows in line:
        temp = rows.strip().split('\n')
        temp = str(temp).strip("['']")
        new_line.append(int(temp))

    print('\nOpening original dataset, please wait.')
    # Pandas Import Original CSV
    p_dataset = pd.read_csv('UNSW-NB15_1.csv', low_memory = False)

    # Creating a null value for the comparison
    null = p_dataset[p_dataset.columns[47]][0]

    # Prints number and names of unique values in malicious packet index
    unique_names = p_dataset[p_dataset.columns[47]].unique()
 
    # Creating workbook to save test set until its written to a csv
    wb = Workbook() 
    sheet1 = wb.add_sheet('Sheet 1') 

    # Declaring variables for trackig packet count and tracking written rows
    counter = 0
    a = 0

    print('\nSaving list of malware packets, please wait.')

    # For loop that gets at most 50 of each type of malware and saves it to a spreadsheet
    for y in range(9):
        counter = 0
        for x in range(22215):
            if p_dataset[p_dataset.columns[47]][new_line[x]] == unique_names[y+1] and counter < 50:
                for z in range(49):
                    sheet1.write(a, z, str(p_dataset[p_dataset.columns[z]][new_line[x]]))
                a += 1
                counter += 1
            elif(counter > 49):
                break

    # Resetting Counter so the next loop is not skipped
    counter = 0

    print('\nSaving list of clean packets, please wait.')

    # For loop that gets at most 50 clean packets and saves to spreadsheet
    for x in range(22215):
        if int(p_dataset[p_dataset.columns[48]][x]) == 0 and counter < 50:
            for z in range(49):
                sheet1.write(a, z, str(p_dataset[p_dataset.columns[z]][x])) 
            a += 1
            counter += 1
        elif(counter > 49):
            break

    # Create new XLS and save values to it
    wb.save('perceptron_test_set.xls') 

    print('\nFile Created: perceptron_test_set.xls')
    print('\nConverting XLS to CSV')
    
    # Converting XLS to CSV
    read_file = pd.read_excel (r'perceptron_test_set.xls', sheet_name='Sheet 1')
    read_file.to_csv (r'perceptron_test_set.csv', index = None, header=True)

    print('\nFile Created: perceptron_test_set.csv')

digest_file()
#make_test_file()