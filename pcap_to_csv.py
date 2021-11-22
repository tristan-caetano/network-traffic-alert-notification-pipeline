# Converts PCAP into CSV, with fields in correct order as specified in example CSV
#not all fields possible but some
import os 
import pyshark
from pyshark import tshark
import pandas as pd
import GUI_print as gp

out_file = "traffic.csv"

gp.print(output, '\nBeginning Conversion')

#os.system('tshark -r test.pcap -T fields -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e _ws.col.protocol -e frame.time_relative -e tcp.analysis.bytes_in_flight -e ip.ttl -e frame.protocols -E separator=,> '+ out_file) #Uses command line argument to read in the PCAP

os.system('tshark -r test.pcap -T fields -e _ws.col.protocol -E separator=, >' + out_file)

gp.print(output, ('\nConversion Complete!\nFile Created: ' + out_file))

# 1. Source IP Address v
# 2. Source Port v
# 3. Destination IP v
# 4. Destination Port v
# 5. Transaction Protocol 
# 6. Time Relative, i.e., Time active
# 7. Transaction Bytes
# 8. Time to live
# 9. Service Protocols


  #0 frame.number - Number of the packet as it appears in the list
  # 1 ip.src - Source IP
  # 3 ip.dst - Destination IP
  # 5 _ws.col.Protocol - Transaction protocol

  # -e ip.src -e tcp.port  udp.port -e ip.dst -e tcp.port  udp.port -e  ip.proto 

  # Ignore Columns: 48, 49