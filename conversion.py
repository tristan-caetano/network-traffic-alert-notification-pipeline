import os

in_file = "small.pcap"
out_file = "traffic.csv"

os.system("tshark -n -r " + in_file + " -T fields -e frame.number -e ip.src -e _ws.col.srcport -e ip.dst -e _ws.col.Protocol -E separator=, -E occurrence=f > " + out_file)

# 0 frame.number - Number of the packet as it appears in the list
# 1 ip.src - Source IP
# 3 ip.dst - Destination IP
# 5 _ws.col.Protocol - Transaction protocol

# -e ip.src -e tcp.port || udp.port -e ip.dst -e tcp.port || udp.port -e  ip.proto 

# Ignore Columns: 48, 49