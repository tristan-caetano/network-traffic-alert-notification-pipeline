# Converts PCAP into CSV, with fields in correct order as specified in example CSV
# Not all fields possible but some

import os
import tkinter as tk
import pyshark
from pyshark import tshark
import pandas as pd
import GUI_print as gp

def convert(output, in_file):
    out_file = "traffic.csv"

    gp.print(output, '\nBeginning Conversion')
    
    os.system('tshark -r small.pcap -T fields -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport  -e frame.protocols -e frame.time_relative -e tcp.analysis.bytes_in_flight -e ip.ttl -e frame.protocols -E separator=,>' + out_file) #Uses command line argument to read in the PCAP

    gp.print(output, ('\nConversion Complete!\nFile Created: ' + out_file))

    return out_file

    # 0 frame.number - Number of the packet as it appears in the list
    # 1 ip.src - Source IP
    # 3 ip.dst - Destination IP
    # 5 _ws.col.Protocol - Transaction protocol

    # -e ip.src -e tcp.port || udp.port -e ip.dst -e tcp.port || udp.port -e  ip.proto 

    # Ignore Columns: 48, 49

    # 1. Source IP Address
    # 2. Source Port
    # 3. Destination IP
    # 4. Destination Port
    # 5. Transaction Protocol
    # 6. Time Relative, i.e., Time active
    # 7. Transaction Bytes
    # 8. Time to live
    # 9. Service Protocols