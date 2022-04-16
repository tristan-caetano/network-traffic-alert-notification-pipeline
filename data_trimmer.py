# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Function that trims the UNSW dataset to match the columns from the PCAP to CSV converter

#  ---------------  Libraries  ---------------
import pandas as pd

def trim(infile):

    # Name of output file
    outfile = "snip_" + infile

    # Choosing what columns to keep from original dataset
    chosen_cols = [7, 8, 10, 21, 35, 48, 49]

    # Choosing what columns to keep from original dataset
    # chosen_cols = [2, 4, 7, 8, 10, 21, 35, 48, 49]

    # TODO: Reset columns (del this line) 
    # chosen_cols = [2, 4, 7, 8, 9, 10, 18, 19, 20, 21, 22, 23, 33, 34, 35, 36, 48, 49]

    # Taking in original dataset
    og_ds = pd.read_csv(infile, low_memory=False)

    # Creating new dataframe for the copied columns
    new_ds = pd.DataFrame()

    # Only adding columns specified in array
    for x in chosen_cols:
        new_ds = pd.concat([new_ds, og_ds[og_ds.columns[x - 1]]], axis=1)

    # Assigning columns
    new_ds.columns = get_cols(True)

    # Saving to file, and making sure an extraneous index isnt added
    new_ds.to_csv(outfile, index=False)

    #gp.print(output, '\nTrimming Complete!\nOutput File: ' + outfile + "\n")

    return outfile

# Setting columns for the pipeline
def get_cols(has_mal):
    if has_mal:
        columns = [ "timerel",      # 7
                    "srctranbytes", # 8
                    "timetolive",   # 10
                    # "dsttosrc",   # 18
                    # "srcwindow",  # 19
                    # "dstwindow",  # 20
                    "srctcp",       # 21
                    # "dstseq",     # 22
                    # "srcmean",    # 23
                    # "setupround", # 33
                    # "setupsynack",# 34
                    "setupackack",  # 35
                    # "ifequal",    # 36
                    "malname",      # 48 
                    "ismal" ]       # 49
    else:
        columns = [
                "srcip",          # 1
                "srcport",        # 2
                "dstip",          # 3
                "dstport",        # 4
                "protocol",       # 5
                "timerel",        # 7
                "srctranbytes",   # 8
                "timetolive",     # 10
                # "dsttosrc",     # 18
                # "srcwindow",    # 19
                # "dstwindow",    # 20
                "srctcp",         # 21
                # "dstseq",       # 22
                # "srcmean",      # 23
                # "setupround",   # 33
                # "setupsynack",  # 34
                "setupackack",    # 35
                # "ifequal",      # 36
                ]

    return columns