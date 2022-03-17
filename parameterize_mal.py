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

    df['malname'] = df['malname'].replace([pd.NA,'Exploits', 'Reconnaissance', 'DoS', 'Generic', 'Shellcode', ' Fuzzers', 'Worms', 'Backdoors', 'Analysis'],['0','1', '2', '3', '4', '5',' 6', '7', '8', '9'])

    df.to_csv("n_"+input, index=False)

change("n_training.csv")
change("n_validation.csv")
change("n_testing.csv")
