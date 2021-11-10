import os
import tkinter as tk

def convert(output, in_file):
    out_file = "traffic.csv"

    output.configure(state='normal')
    output.insert(tk.END, '\nBeginning Conversion')
    output.see(tk.END)
    output.configure(state='disabled')
    output.update()

    os.system("tshark -n -r " + in_file + " -T fields -e ip.src -e _ws.col.srcport -e ip.dst -e _ws.col.Protocol -e ip.version -e ip.hdr_len -e ip.tos -e ip.id -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum -e ip.len -e ip.dsfield -e tcp.srcport -E separator=, -E occurrence=f > " + out_file)

    output.configure(state='normal')
    output.insert(tk.END, '\nConversion Complete!\nFile Created: ' + out_file)
    output.see(tk.END)
    output.configure(state='disabled')
    output.update()

    # 0 frame.number - Number of the packet as it appears in the list
    # 1 ip.src - Source IP
    # 3 ip.dst - Destination IP
    # 5 _ws.col.Protocol - Transaction protocol

    # -e ip.src -e tcp.port || udp.port -e ip.dst -e tcp.port || udp.port -e  ip.proto 

    # Ignore Columns: 48, 49