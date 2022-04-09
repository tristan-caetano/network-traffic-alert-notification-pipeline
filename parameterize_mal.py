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

def change(input):

    count = 0
    outputs = ["", "", ""]

    # For loop that parameterizes each file
    for files in input:

        # Pandas Import CSV
        df = pd.read_csv(files, low_memory=False)

        df['malname'] = df['malname'].replace([pd.NA,'Exploits', 'Reconnaissance','Reconnaissance ', ' Reconnaissance ', 'DoS', 'Generic', ' Fuzzers'],['0','1', '2', '2', '2', '3', '4', '5'])
        #df['malname'] = df['malname'].replace([pd.NA,'Exploits', 'Reconnaissance','Reconnaissance ', 'DoS', 'Generic', ' Fuzzers', 'Shellcode', 'Worms', 'Backdoors', 'Analysis'],['0','1', '2', '2', '3', '4', '5', '6', '7', '8', '9'])

        # Saving file names to be returned and exporting files
        outputs[count] = "p_" + files
        df.to_csv(outputs[count], index=False)
        count += 1

    return outputs

# change("training.csv")
# change("validation.csv")
# change("testing.csv")
