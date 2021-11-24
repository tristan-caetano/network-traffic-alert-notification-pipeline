# Converts PCAP into CSV, with fields in correct order as specified in example CSV
#not all fields possible but some
import os 
import pyshark
from pyshark import tshark
import pandas as pd
import GUI_print as gp

def convert(output, in_file):

  out_file = "converted.csv"

  gp.print(output, '\nBeginning Conversion\nThis may take a bit')

  os.system('tshark -r ' + in_file + ' -T fields -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e _ws.col.Protocol -e frame.time_relative -e tcp.analysis.bytes_in_flight -e ip.ttl -e tcp.seq -e tcp.ack -E separator=,> '+ out_file) #Uses command line argument to read in the PCAP

  gp.print(output, ('\nConversion Complete!\nFile Created: ' + out_file + '\nOpening File in GUI...'))

  return out_file

    # 1. Source IP Address v 1
    # 2. Source Port v 2
    # 3. Destination IP v 3
    # 4. Destination Port v 4
    # 5. Transaction Protocol 5
    # 6. Time Relative, i.e., Time active 7
    # 7. Transaction Bytes 8
    # 8. Time to live 10
    # 9. 21
    # 10. 35

    # 0 frame.number - Number of the packet as it appears in the list
    # 1 ip.src - Source IP
    # 3 ip.dst - Destination IP
    # 5 _ws.col.Protocol - Transaction protocol

    # -e ip.src -e tcp.port  udp.port -e ip.dst -e tcp.port  udp.port -e  ip.proto 

    # Ignore Columns: 48, 49