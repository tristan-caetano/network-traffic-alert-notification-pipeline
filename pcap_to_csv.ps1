# Powershell script that is run from pcap_to_csv.py if the GUI is being run on windows    
    
    # Taking in the names of the input pcap and output csv
    param(
        $wInput,
        $wOutput
    )

    # Running the tshark command from the tshark.exe found in the default install directory
    & 'C:\Program Files\Wireshark\tshark.exe' -r $wInput -T fields -E separator="," -e tcp.srcport -e tcp.dstport -e frame.time_relative -e tcp.analysis.bytes_in_flight -e ip.ttl -e tcp.seq -e tcp.ack > $wOutput