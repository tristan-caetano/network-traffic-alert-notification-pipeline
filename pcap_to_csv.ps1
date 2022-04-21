# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Powershell script that is run from pcap_to_csv.py if the GUI is being run on windows    
    
    # Taking in the names of the input pcap and output csv
    param(
        $wInput,
        $wOutput
    )

    # Running the tshark command from the tshark.exe found in the default install directory
    & 'C:\Program Files\Wireshark\tshark.exe' -r $wInput -T fields -E separator="," -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e _ws.col.Protocol -e frame.time_relative -e frame.len -e ip.ttl -e tcp.seq -e tcp.ack > $wOutput