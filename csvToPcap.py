import pyshark
from pyshark import tshark

pcap = pyshark.FileCapture('test.pcap')

for pkt in pcap:

    #print(pkt.captured_length) #???
    #print(pkt.transport_layer) #Protocol
    print(pkt.sniff_time) #Time
    #print(pkt.length) #Length
    




#print(pcap)

#for packet in pcap:
# print(pcap[0][0])
#print(pcap[0])
#print(pcap[0]['sll'])

# print(pcap[0]['ip'])
# print(pcap[0]['tcp'])

# print("\n")
# print("Source IP:\t", pcap[0]['ip'].src)
# print("Destination IP:\t", pcap[0]['ip'].dst)
# print("Unused:\t\t", pcap[0][0].Unused)
