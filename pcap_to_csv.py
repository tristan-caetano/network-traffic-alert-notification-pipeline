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
import pandas as pd
import GUI_print as gp

# Function that converts pcap to csv
def convert(output, in_file):

  # Name of csv output file
  out_file = "converted.csv"

  gp.print(output, '\nBeginning Conversion\nThis may take a bit')

  # Using TShark to extract the PCAP parameters
  os.system('tshark -r ' + in_file + ' -T fields -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e _ws.col.Protocol -e frame.time_relative -e tcp.analysis.bytes_in_flight -e ip.ttl -e tcp.seq -e tcp.ack -E separator=,> '+ out_file) #Uses command line argument to read in the PCAP

  gp.print(output, ('\nConversion Complete!\nFile Created: ' + out_file + '\nOpening File in GUI...'))

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

  # Ignore Columns: 48, 49