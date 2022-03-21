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
from sklearn import preprocessing
import GUI

# Creating CSV test set for Multilayer Perceptron
def digest_file(infile, gui_self):

    outfile_name = "n_" + infile

    GUI.SettingsWindow.updateMessage(gui_self, 60, "Reading parameterized file.")

    # Pandas Import CSV
    p_dataset = pd.read_csv(infile, low_memory=False, encoding= "utf-16")

    GUI.SettingsWindow.updateMessage(gui_self, 70, "Normalizing dataset.")

    # Min Max Normalization
    t_df = p_dataset.values
    min_max_scaler = preprocessing.MinMaxScaler()
    t_df_scaled = min_max_scaler.fit_transform(t_df)
    n_df = pd.DataFrame(t_df_scaled)

    n_df = n_df.rename(columns={
                0: "srcport",
                1: "dstport",
                2: "timerel", 
                3: "tranbytes", 
                4: "timetolive", 
                5: "srctcp", 
                6: "dsttcp"})

    GUI.SettingsWindow.updateMessage(gui_self, 80, "Saving normalized file.")

    # Save new normalized CSV file
    n_df.to_csv(outfile_name, index=True)
    print(n_df)

    # Returning name of csv file
    return outfile_name

# digest_file("n_n_testing.csv", 0)
# digest_file("n_n_testing.csv", 0)
# digest_file("n_n_testing.csv", 0)