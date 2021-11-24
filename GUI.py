#  ---------------  Libraries  ---------------
import tkinter as tk
import create_test_set as cts
from parameterizer import parameterize
import pcap_to_csv as cv
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
import os.path
import threading
import csv
import GUI_print as gp
import data_trimmer as dt
import pandas as pd
import parameterizer as pm

win= Tk()

outputname = StringVar()
csvname = StringVar()
outputname.set("Output:")
csvname.set("CSV")

# Resize window
win.geometry("1920x1080")
win.title("Network Traffic Alert Notification Pipeline​ GUI")

# This is what happens when you click the import button.
def import_box(event=None):
   global filename
   filename = filedialog.askopenfilename()
   filename = os.path.basename(filename)
   output.configure(state='normal')
   my_str = filename[-5:]
   if my_str == ".pcap":
      output.insert(tk.END, 'Selected PCAP: ')
      output.insert(tk.END, filename)
      output.insert(tk.END, '\n')
      output.see(tk.END)
      output.configure(state='disabled')
   else:
      output.insert(tk.END, 'File is not a PCAP\n')
      output.see(tk.END)
      output.configure(state='disabled')

def import_box2(event=None):
   global filenameCSV
   filenameCSV = filedialog.askopenfilename()
   filenameCSV = os.path.basename(filenameCSV)

   # The if-statement and else-statement detects if the file is a CSV or not.
   my_str = filenameCSV[-4:]
   output.configure(state='normal')
   if my_str == ".csv":
      output.insert(tk.END, 'Selected CSV file: ')
      output.insert(tk.END, filenameCSV)
      output.insert(tk.END, '\n')
      output.see(tk.END)
      output.configure(state='disabled')
   else:
      output.insert(tk.END, 'File is not a CSV\n')
      output.see(tk.END)
      output.configure(state='disabled')

# This is what happens when you click the GO button.
def start(event=None):
   outputname.set("Output: Converting PCAP to CSV...")
   print('start conversion')
   output.configure(state='normal')
   output.delete(1.0, END)
   output.insert(tk.END, 'Starting Conversion...\n')
   output.see(tk.END)
   print("eqefwfwefwe: ", filename)
   output.configure(state='disabled')
   curr_csv = cv.convert(output, filename)
   print("dfsfdsfds: ", curr_csv)
   show_csv(curr_csv)
   outputname.set("Output:")
   # Call the conversion script
   
#this is what happens when you click the clear button
def clear_output(event=None):
   print('output clear event')
   output.configure(state='normal')
   output.delete(1.0, END)
   output.configure(state='disabled')

# This is what happens when you click the CREATE TEST SET
def create_set(event=None):
   outputname.set("Output: Creating test set...")
   print('start create test set')
   output.configure(state='normal')
   output.delete(1.0, END)
   output.insert(tk.END, 'Creating Test Set...\n')
   output.see(tk.END)
   output.configure(state='disabled')
   print("Running...: ", filenameCSV)
   print(type(filenameCSV))
   curr_csv = cts.digest_file(filenameCSV, output)
   show_csv(curr_csv)
   outputname.set("Output:")
   # Call the script using filenameCSV

   # This is what happens when you click the Trim Data Set
def trim_dataset(event=None):
   outputname.set("Output: Trimming Data Set...")
   print('start create test set')
   gp.print(output, '\nTrimming Data Set...\n')
   print("Running...: ", filenameCSV)
   print(type(filenameCSV))
   curr_csv = dt.trim(filenameCSV, output)
   show_csv(curr_csv)
   outputname.set("Output:")
   # Call the script using filenameCSV

      # This is what happens when you click the Trim Data Set
def parameterize(event=None):
   outputname.set("Output: Parameterizing converted dataset...")
   print('start create test set')
   gp.print(output, '\nParameterizing converted dataset...\n')
   print("Running...: ", filenameCSV)
   print(type(filenameCSV))
   curr_csv = pm.parameterize(filenameCSV, output)
   show_csv(curr_csv)
   outputname.set("Output:")
   # Call the script using filenameCSV

#CSV view
def show_csv(csvfile):
   csvname.set("CSV: "+str(csvfile))
   #global importflag
   #if importflag==1:           yea dunno if this is needed
   #   tree.destroy()
   TableMargin = Frame(win, width=16)
   TableMargin.place(x=650, y=60)
   scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
   scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
   tree = ttk.Treeview(TableMargin, columns=("ip src", "port src", "ip dest", "port dest", "protocol", "active time", "bytes", "live time", "src tcp bsn", "tcp cst", "mal packet type", "is mal?"), height=32, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
   scrollbary.config(command=tree.yview)
   scrollbary.pack(side=RIGHT, fill=Y)
   scrollbarx.config(command=tree.xview)
   scrollbarx.pack(side=BOTTOM, fill=X)
   tree.heading('ip src', text="ip src", anchor=W)
   tree.heading('port src', text="port src", anchor=W)
   tree.heading('ip dest', text="ip dest", anchor=W)
   tree.heading('port dest', text="port dest", anchor=W)
   tree.heading('protocol', text="protocol", anchor=W)
   tree.heading('active time', text="active time", anchor=W)
   tree.heading('bytes', text="bytes", anchor=W)
   tree.heading('live time', text="live time", anchor=W)
   tree.heading('src tcp bsn', text="src tcp bsn", anchor=W)
   tree.heading('tcp cst', text="tcp cst", anchor=W)
   tree.heading('mal packet type', text="mal packet type", anchor=W)
   tree.heading('is mal?', text="is mal?", anchor=W)
   tree.column('#0', stretch=NO, minwidth=0, width=0)
   tree.column('#1', stretch=NO, minwidth=0, width=100)
   tree.column('#2', stretch=NO, minwidth=0, width=60)
   tree.column('#3', stretch=NO, minwidth=0, width=100)
   tree.column('#4', stretch=NO, minwidth=0, width=60)
   tree.column('#5', stretch=NO, minwidth=0, width=80)
   tree.column('#6', stretch=NO, minwidth=0, width=100)
   tree.column('#7', stretch=NO, minwidth=0, width=60)
   tree.column('#8', stretch=NO, minwidth=0, width=60)
   tree.column('#9', stretch=NO, minwidth=0, width=100)
   tree.column('#10', stretch=NO, minwidth=0, width=60)
   tree.column('#11', stretch=NO, minwidth=0, width=100)
   tree.pack()

   rows = []

   with open(csvfile) as f:
      reader = csv.reader(f, delimiter=',')
      
      # This works, buts its incredibly slow
      for row in reader:
         print(row)           #use pandas to get each of these column names (just here tho everywhere else is ok)
         tree.insert("", 0, values=row)

   importflag = 1

# Create labels
Label(win, text= "Network Traffic Alert Notification Pipeline​ GUI").pack(pady= 10)
Label(win, textvariable= str(outputname)).place(x=50, y=184)
Label(win, textvariable= str(csvname)).place(x=700, y=40)

# Create buttons
ttk.Button(win, text= "Import PCAP", command=import_box).place(x=50, y=40)
ttk.Button(win, text= "Convert to CSV", command=start).place(x=50, y=80)
ttk.Button(win, text= "Clear Output", command=clear_output).place(x=50, y=150)
ttk.Button(win, text= "Import CSV", command=import_box2).place(x=280, y=40)
ttk.Button(win, text= "Create Test Set", command=create_set).place(x=180, y=80)
ttk.Button(win, text= "Trim Data Set", command=trim_dataset).place(x=280, y=80)
ttk.Button(win, text= "Parameterize", command=parameterize).place(x=369, y=80)

# Output window

output = Text(win, state = 'disabled', width=80, height=36)
output.place(x=50, y=204)



# start window
win.mainloop()
