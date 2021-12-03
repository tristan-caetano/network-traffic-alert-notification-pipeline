#  ---------------  Libraries  ---------------
import tkinter as tk
import create_test_set as cts
from parameterizer import parameterize
import pcap_to_csv as cv
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
import os
import os.path
import threading
import csv
import GUI_print as gp
import data_trimmer as dt
import pandas as pd
import parameterizer as pm

#Initialize window and global variables
win= Tk()
outputname = StringVar()
csvname = StringVar()
outputname.set("Output:")
csvname.set("CSV")

#Resize window
win.geometry("1920x1080")
win.title("Network Traffic Alert Notification Pipeline​")

#clear output window
def clear_output(event=None):
   output.configure(state='normal')
   output.delete(1.0, END)
   output.configure(state='disabled')

#CSV file importer
def import_CSV(event=None):
   global filenameCSV
   filenameCSV = filedialog.askopenfilename()
   filenameCSV = os.path.basename(filenameCSV)

   #Detects if the file is a CSV or not
   filetype = filenameCSV[-4:]
   if filetype == ".csv":
      gp.print(output, '\nSelected CSV file:')
      gp.print(output, filenameCSV)
      return 0
   else:
      gp.print(output, '\nFile is not a CSV')
      return 1

#Convert to PCAP
def convert_pcap(event=None):
   global filename
   filename = filedialog.askopenfilename()
   filename = os.path.basename(filename)
   filetype = filename[-5:]
   #Detects if the file is a PCAP or not.
   if filetype == ".pcap":
      outputname.set("Output: Converting PCAP to CSV...")
      clear_output()
      gp.print(output, '\nStarting Conversion...')
      curr_csv = cv.convert(output, filename)
      show_csv(curr_csv)
      outputname.set("Output:")
   else:
      gp.print(output, '\nFile is not a PCAP')

#Create test set
def create_set(event=None):
   if import_CSV()==0:
      outputname.set("Output: Creating test set")
      clear_output()
      gp.print(output, '\nCreating Test Set...')
      curr_csv = cts.digest_file(filenameCSV, output)
      show_csv(curr_csv)
      outputname.set("Output:")

#Trim Data Set
def trim_dataset(event=None):
   if import_CSV()==0:
      outputname.set("Output: Trimming Data Set")
      clear_output()
      gp.print(output, '\nTrimming Data Set...')
      curr_csv = dt.trim(filenameCSV, output)
      show_csv(curr_csv)
      outputname.set("Output:")

#Parameterize
def parameterize(event=None):
   if import_CSV()==0:
      outputname.set("Output: Parameterizing")
      clear_output()
      gp.print(output, '\nParameterizing converted dataset...')
      curr_csv = pm.parameterize(filenameCSV, output)
      show_csv(curr_csv)
      outputname.set("Output:")

def show_help(event=None):
   showinfo(title='Using the GUI', message="PCAP to CSV Pipeline:\n1. Click PCAP->CSV and select the PCAP file you wish to convert.\n2. Click Parameterize and select the converted CSV file to change all strings to integers.\n\nTest Set Pipeline:\n1. Click Trim Data Set and select the CSV file you wish to trim.\n2. Click CSV->Test Set and select the CSV file to create a test set. (must be parameterized)")

#CSV view
def show_csv(csvfile):
   csvname.set("CSV: "+str(csvfile))
   TableMargin = Frame(win, width=16)
   TableMargin.place(x=700, y=60)
   scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
   scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
   tree = ttk.Treeview(TableMargin, columns=("ip src", "port src", "ip dest", "port dest", "protocol", "active time", "bytes", "live time", "src tcp bsn", "tcp cst", "mal packet type", "is mal?"), height=41, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
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

   with open(csvfile) as f:
      reader = csv.reader(f, delimiter=',')
      for row in reader:
         tree.insert("", 0, values=row)

#Create labels and divider line
Label(win, text= "Network Traffic Alert Notification Pipeline​ GUI").pack(pady= 10)
Label(win, text= "PCAP to CSV Pipeline").place(x=30, y=40)
Label(win, text= "Test Set Pipeline").place(x=250, y=40)
Label(win, textvariable= str(outputname)).place(x=30, y=184)
Label(win, textvariable= str(csvname)).place(x=700, y=40)
seperator=ttk.Separator(win, orient='vertical')
seperator.place(x=210,y=44,height=120)

#Create buttons
ttk.Button(win, text= "Convert PCAP->CSV", command=convert_pcap).place(x=30, y=70,height=40)
ttk.Button(win, text= "Parameterize", command=parameterize).place(x=30, y=120,height=40)
ttk.Button(win, text= "Trim Data Set", command=trim_dataset).place(x=250, y=70,height=40)
ttk.Button(win, text= "CSV->Test Set", command=create_set).place(x=250, y=120,height=40)
ttk.Button(win, text= "Help", command=show_help).place(x=30, y=5,height=25)

#Output window
output = Text(win, state = 'disabled', width=80, height=41)
output.place(x=30, y=204)

#Start GUI
win.mainloop()
