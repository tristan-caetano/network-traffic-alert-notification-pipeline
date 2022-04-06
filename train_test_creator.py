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
import numpy as np
import math

# Creating file that contains all the row number mal packets from the UNSW-NB15_1M.csv dataset 
# THIS SHOULD ONLY HAVE TO BE RUN ONCE PER FILE
def determine_packet_allocation(dataset, num_of_packets, class_column):
# 10000 packets

    # Getting amount of packets for each set (80%: 80% train / 20% validation)(20% testing)
    # training = math.floor((num_of_packets * 80) / 100)
    # testing = math.floor((num_of_packets * 20) / 100)
    # validation = math.floor((training * 20) / 100)
    # training = training - validation
    training = 64
    testing = 20
    validation = 16
    
    # Saving values to array for passing into functions
    percentages = [training, testing, validation]

    # Pandas Import CSV
    p_dataset = pd.read_csv(dataset, low_memory=False)
    p_dataset = p_dataset.rename(columns={
    "1390": "srcport",
    "53": "dstport",
    "0.001055": "timerel", 
    "132": "tranbytes", 
    "31": "timetolive", 
    "0.4": "srctcp", 
    "0.12": "dsttcp", 
    "Unnamed: 47": "malname", 
    "0.18": "ismal"})

    # Prints number and names of unique values in malicious packet index
    unique_names = p_dataset[p_dataset.columns[class_column]].unique()

    unique_names = np.delete(unique_names, 5)
    unique_names = np.delete(unique_names, 6)
    unique_names = np.delete(unique_names, 6)
    unique_names = np.delete(unique_names, 6)
    unique_names = np.delete(unique_names, 6)
    unique_names = np.delete(unique_names, 6)
    
    print(unique_names)
    
    # How many of each packet should be in the dataframe
    per_packet = math.floor(num_of_packets / len(unique_names))

    # Counter to make sure that each packet amount is not more than per_packet
    count = 0

    # Keeping track of which packet in unique_packets is being stored
    current_packet = 0

    # Array of dataframes that contain each type of packet
    amt_of_each_mal = [None] * len(unique_names)

    # Creating temp df to store values before being saved to df array
    temp_df = pd.DataFrame()

    # Initializing index
    x = 0

    print("Getting all mal packets")
    # An while loop that fills amt_of_each_packets with the packets that are needed
    while x < len(p_dataset):

        # If the limit of packets of that type have been reached, or if the whole dataset has been checked through
        if count == per_packet or x == (len(p_dataset) - 1):

            print("Count: ", count, " Per Packet: ", per_packet, "Packet Type: ", unique_names[current_packet])
            count = 0
            amt_of_each_mal[current_packet] = temp_df
            temp_df = pd.DataFrame(columns=[
                "srcport",
                "dstport",
                "timerel", 
                "tranbytes", 
                "timetolive", 
                "srctcp", 
                "dsttcp", 
                "malname", 
                "ismal"])

            current_packet += 1
            x = 0         

        unjunk = [5,6]
        
        # Making sure we haven't already done all the packet types
        if(current_packet <= len(unique_names) - 1):

            # If the current row contains the packet type we are looking for, save it
            # MIGHT NEED TO BE AN ELSE IF
            if (str(unique_names[current_packet]) in str(p_dataset[p_dataset.columns[class_column]][x])) or (pd.isna(p_dataset[p_dataset.columns[class_column]][x]) and pd.isna(unique_names[current_packet])):
                
                if p_dataset[p_dataset.columns[unjunk[0]]][x] != p_dataset[p_dataset.columns[unjunk[1]]][x]:
                    temp_df = temp_df.append(p_dataset.iloc[x])
                    count += 1

        # Forcing the loop to complete
        else: x = len(p_dataset) + 1
        
        # Incrementing index
        x += 1

    
    print(amt_of_each_mal)

    # Sending data to be split into csvs
    create_data_sets(amt_of_each_mal, percentages)

#
def create_data_sets(amt_of_each_mal, percentages):
    
    print("Splitting datasets")

    # 1: training 64%, 2: validation 16%, 3: testing 20%
    training_sets = [pd.DataFrame(columns=[
                "srcport",
                "dstport",
                "timerel", 
                "tranbytes", 
                "timetolive", 
                "srctcp", 
                "dsttcp", 
                "malname", 
                "ismal"])] * 3
    
    amt_per_df = [0] * len(amt_of_each_mal)
    starting_points = [0] * len(amt_of_each_mal)

    for z in range(len(amt_of_each_mal)):

        amt_per_df[z] = len(amt_of_each_mal[z])

    for a in range(len(training_sets)):
        print("SetL ", a)

        for x in range(len(amt_of_each_mal)):
                
            curr_amt = math.floor((amt_per_df[x] * percentages[a]) / 100)
                
            for b in range(starting_points[x], (starting_points[x] + curr_amt)):
                
                training_sets[a] = training_sets[a].append(amt_of_each_mal[x].iloc[b])
            starting_points[x] += curr_amt

    training_sets[0].to_csv("training.csv", index=False)
    training_sets[1].to_csv("validation.csv", index=False)
    training_sets[2].to_csv("testing.csv", index=False)
    
determine_packet_allocation("snip_UNSW-NB15_com.csv", 18000, 7)
