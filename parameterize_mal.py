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
import pandas as pd

# Will parameterize the malicious names of the mal type
def change(input):

    # Initializing count and output variables
    count = 0
    outputs = ["", "", ""]

    # For loop that parameterizes each file
    for files in input:

        # Pandas Import CSV
        try:
            df = pd.read_csv(files, low_memory=False, encoding= "utf-8")
        except:
            df = pd.read_csv(files, low_memory=False, encoding= "utf-16")

        # Used packets (Multiple name copies for slight changes in the UNSW dataset)
        df['malname'] = df['malname'].replace([pd.NA,'Exploits', 'Reconnaissance','Reconnaissance ', ' Reconnaissance ', 'DoS', 'Generic', ' Fuzzers'],['0','1', '2', '2', '2', '3', '4', '5'])

        # Saving file names to be returned and exporting files
        outputs[count] = "p_" + files
        df.to_csv(outputs[count], index=False)
        count += 1

    return outputs

# Reverse parameterization after predictions are completed
def rev_param(in_file):

    # Pandas Import CSV
    try:
        df = pd.read_csv(in_file, low_memory=False, encoding= "utf-8")
    except:
        df = pd.read_csv(in_file, low_memory=False, encoding= "utf-16")

    # Used packets (Multiple name copies for slight changes in the UNSW dataset)
    df['predictions'] = df['predictions'].replace([0, 1, 2, 3, 4, 5], ['Clean', 'Exploits', 'Reconnaissance', 'DoS', 'Generic', 'Fuzzers'])

    # Overwriting csv
    df.to_csv(in_file, index=False)