import csv
import pandas as pd
import xlwt 
from pandas.core.arrays.sparse import dtype
from xlwt import Workbook

# Creating file that contains all the row number mal packets from the UNSW-NB15_1.csv dataset 
# THIS SHOULD ONLY HAVE TO BE RUN ONCE PER FILE
def digest_file():
    
    # Pandas Import CSV
    p_dataset = pd.read_csv('UNSW-NB15_1.csv')

    # Creating dataset from CSV data
    dataframe = pd.DataFrame(p_dataset)

    # These arrays will contain the number of each malware type and each row that contains a malicious packet respectively
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    usable_rows = []

    # Prints number and names of unique values in malicious packet index
    unique_vals = p_dataset[p_dataset.columns[47]].nunique()
    unique_names = p_dataset[p_dataset.columns[47]].unique()
    print(unique_vals)
    print(unique_names)

    # Creating a null value for the comparison
    null = p_dataset[p_dataset.columns[47]][0]

    # For loops that populate the respective arrays
    for x in range(700000):
        print(x)
        for y in range(10):
            if p_dataset[p_dataset.columns[47]][x] == unique_names[y] and p_dataset[p_dataset.columns[47]][x] != null:
                arr[y] += 1
                usable_rows.append(x)

    # Writing the rows numbers to a file to avoid sifting through the entire dataset repeatedly
    f = open('list_of_rows.txt', 'w')
    for rows in usable_rows:
        f.write(str(rows) + "\n")
    f.close()

    # printing array for verification
    print(arr)

def make_test_file():
    r = open('list_of_rows.txt', 'r')
    line = r.readlines()
    new_line = []
    for rows in line:
        temp = rows.strip().split('\n')
        temp = str(temp).strip("['']")
        new_line.append(int(temp))

    # Pandas Import CSV
    p_dataset = pd.read_csv('UNSW-NB15_1.csv', low_memory = False)

    # Creating a null value for the comparison
    null = p_dataset[p_dataset.columns[47]][0]

    # Prints number and names of unique values in malicious packet index
    unique_names = p_dataset[p_dataset.columns[47]].unique()

    wb = Workbook() 
    sheet1 = wb.add_sheet('Sheet 1') 
    counter = 0
    a = 0

    for y in range(10):
        counter = 0
        for x in range(22215):
            if p_dataset[p_dataset.columns[47]][unique_names[x]] == unique_names[y] and p_dataset[p_dataset.columns[47]][unique_names[x]] != null and counter < 50:
                for y in range(49):
                    # Write row here
                    sheet1.write(a, y, p_dataset[p_dataset.columns[x]][y]) 
                    a += 1
                    counter += 1

    wb.save('perceptron_test_set.csv') 

#digest_file()
make_test_file()