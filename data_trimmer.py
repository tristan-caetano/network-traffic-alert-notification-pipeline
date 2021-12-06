# Network Traffic Alert Notification Pipeline Documentation Project MVP 
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
import tkinter as tk
import pandas as pd
import GUI_print as gp

def trim(infile, output):

    # Name of output file
    outfile = "testsnip.csv"

    # Choosing what columns to keep from original dataset
    chosen_cols = [1, 2, 3, 4, 5, 7, 8, 10, 21, 35, 48, 49]

    # Taking in original dataset
    og_ds = pd.read_csv(infile, low_memory=False)

    # Creating new dataframe for the copied columns
    new_ds = pd.DataFrame()

    # Only adding columns specified in array
    for x in chosen_cols:
        new_ds = pd.concat([new_ds, og_ds[og_ds.columns[x - 1]]], axis=1)

    # Saving to file, and making sure an extraneous index isnt added
    new_ds.to_csv(outfile, index=False)

    gp.print(output, '\nTrimming Complete!\nOutput File: ' + outfile + "\n")

    return outfile
