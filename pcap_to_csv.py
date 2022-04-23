# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Converts PCAP into CSV, with fields in correct order as specified in example CSV

#  ---------------  Libraries  ---------------
import os 
import pyshark
from pyshark import tshark
import platform
import GUI
import pandas as pd
import data_trimmer as dt

# Function that converts pcap to csv
def convert(in_file, gui_self):

  # Name of csv output file
  out_file = in_file + ".csv"

  GUI.SettingsWindow.updateMessage(gui_self, 10, "Using TShark on pcap file")

  # Run this command if on Linux
  if platform.system() == "Linux":
    # Using TShark to extract the PCAP parameters
    os.system('tshark -r ' + in_file + ' -T fields -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e _ws.col.Protocol -e frame.time_relative -e frame.len -e ip.ttl -e tcp.seq -e tcp.ack -E separator=,> '+ out_file) #Uses command line argument to read in the PCAP

  # Run this command if on Windows
  elif platform.system() == "Windows":
    temp_command = "powershell -file pcap_to_csv.ps1 -wInput "+in_file+" -wOutput "+out_file+""
    os.system(temp_command)
  
  GUI.SettingsWindow.updateMessage(gui_self, 20, "Creating CSV file")

  # It should be noted through observation of the converter that the .pcap files
  # converted through Linux have a .csv output with utf-8 encoding, however, when 
  # converted through Windows, the .csv output has utf-16 encoding.  

  # Pandas Import CSV to remove null values and add column headers
  try:
    ds = pd.read_csv(out_file, low_memory=False, encoding= "utf-8")
  except:
    ds = pd.read_csv(out_file, low_memory=False, encoding= "utf-16")

  # Filling null values with 0
  ds.fillna(value = 0, inplace = True)

  # Getting column names
  ds.columns = dt.get_cols(False)

  # Outputting file to csv
  ds.to_csv(out_file, index=False)

  return out_file

  # Field names used
    # 1. Source IP Address 1
    # 2. Source Port 2
    # 3. Destination IP 3
    # 4. Destination Port 4
    # 5. Transaction Protocol 5
    # 6. Time Relative, i.e., Time active 7
    # 7. Transaction Bytes 8
    # 8. Time to live 10
    # 9. Source TCP Base Seq Number 21
    # 10. TCP connection setup time, the time between the SYN_ACK and the ACK packets 35