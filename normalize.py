# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Data Normalizer

#  ---------------  Libraries  ---------------
import pandas as pd
import data_trimmer as dt
from sklearn import preprocessing
import GUI

# Creating CSV test set for Multilayer Perceptron
def digest_file(infile, gui_self):

    # Setting the outfile name
    outfile_name = "n_" + infile

    if gui_self is not 0: GUI.SettingsWindow.updateMessage(gui_self, 30, "Reading file for normalization.")

    # Pandas Import CSV
    try:
        p_dataset = pd.read_csv(infile, low_memory=False, encoding= "utf-8")
    except:
        p_dataset = pd.read_csv(infile, low_memory=False, encoding= "utf-16")

    # Dropping columns that arent used in converted set
    if gui_self is not 0: 
        p_dataset = p_dataset.drop([
                    "srcip",          # 1
                    "srcport",        # 2
                    "dstip",          # 3
                    "dstport",        # 4
                    "protocol"        # 5
                    ], axis = 1)

    if gui_self is not 0: GUI.SettingsWindow.updateMessage(gui_self, 40, "Normalizing dataset")

    # Min Max Normalization
    t_df = p_dataset.values
    min_max_scaler = preprocessing.MinMaxScaler()
    t_df_scaled = min_max_scaler.fit_transform(t_df)
    n_df = pd.DataFrame(t_df_scaled)

    if gui_self is not 0: GUI.SettingsWindow.updateMessage(gui_self, 50, "Saving normalized file")

    # Save new normalized CSV file
    if gui_self is 0: n_df.columns = dt.get_cols(True)
    n_df.to_csv(outfile_name, index=False)

    # Returning name of csv file
    return outfile_name