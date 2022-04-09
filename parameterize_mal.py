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

    # Pandas Import CSV
    df = pd.read_csv(input, low_memory=False)

    df['malname'] = df['malname'].replace([pd.NA,'Exploits', 'Reconnaissance','Reconnaissance ', ' Reconnaissance ', 'DoS', 'Generic', ' Fuzzers'],['0','1', '2', '2', '2', '3', '4', '5'])
    #df['malname'] = df['malname'].replace([pd.NA,'Exploits', 'Reconnaissance','Reconnaissance ', 'DoS', 'Generic', ' Fuzzers', 'Shellcode', 'Worms', 'Backdoors', 'Analysis'],['0','1', '2', '2', '3', '4', '5', '6', '7', '8', '9'])

    df.to_csv("p_" + input, index=False)

# change("training.csv")
# change("validation.csv")
# change("testing.csv")

change("training.csv")
change("validation.csv")
change("testing.csv")
