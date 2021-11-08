#Converts PCAP to CSV by first converting to JSON as an intermediary

# Not tested with full size PCAP file due to system constraints
import os 
import pyshark
from pyshark import tshark
import pandas as pd


os.system('tshark -r small.pcap -T json > temp.json') #Uses command line argument to read in the PCAP

pdObj = pd.read_json('temp.json') # Reads JSON file

pdObj.to_csv('output.csv',index = False) # Converts JSON to CSV