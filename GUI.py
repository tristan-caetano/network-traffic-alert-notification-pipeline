#  ---------------  Libraries  ---------------
import tkinter as tk
import create_test_set as cts
import conversion as cv
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
import os.path
import threading
import csv
import pandas as pd

win= Tk()
global tree

# Resize window
win.geometry("1200x800")
win.title("cool gui for cool boys")

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
   print('start conversion')
   output.configure(state='normal')
   output.insert(tk.END, 'Starting Conversion...\n')
   output.see(tk.END)
   output.configure(state='disabled')
   curr_csv = cv.convert(output, filename)
   show_csv(curr_csv)
   # Call the conversion script
   
#this is what happens when you click the clear button
def clear_output(event=None):
   print('output clear event')
   output.configure(state='normal')
   output.delete(1.0, END)
   output.configure(state='disabled')

# This is what happens when you click the CREATE TEST SET
def create_set(event=None):
   print('start create test set')
   output.configure(state='normal')
   output.insert(tk.END, 'Creating Test Set...\n')
   output.see(tk.END)
   output.configure(state='disabled')
   print("Running...: ", filenameCSV)
   print(type(filenameCSV))
   curr_csv = cts.digest_file(filenameCSV, output)
   show_csv(curr_csv)
   # Call the script using filenameCSV

# Create labels
Label(win, text= "WORLDS GREATEST GUI").pack(pady= 10)
Label(win, text= "OUTPUT:").place(x=50, y=184)
Label(win, text= "CSV:").place(x=400, y=20)

# Create buttons
ttk.Button(win, text= "Import PCAP", command=import_box).place(x=50, y=40)
ttk.Button(win, text= "Convert to CSV", command=start).place(x=50, y=80)
ttk.Button(win, text= "Clear Output", command=clear_output).place(x=50, y=150)
ttk.Button(win, text= "Import CSV", command=import_box2).place(x=180, y=40)
ttk.Button(win, text= "Create Test Set", command=create_set).place(x=180, y=80)

# Output window

output = Text(win, state = 'disabled', width=40, height=36)
output.place(x=50, y=204)



#CSV view
def show_csv(csvfile):
   # if tree.winfo_exists() == 1:
   #    tree.destroy()

   # Taking in CSV data and creating a dataframe
   csv = pd.read_csv(csvfile, low_memory=False) 
   dataframe = pd.DataFrame(csv)
   # print(dataframe[dataframe.columns[0]][0])

   col_names = []

   for col in dataframe:
      col_names.append(dataframe[col])
   
   TableMargin = Frame(win, width=100)
   TableMargin.place(x=400, y=40)

   scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
   scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
   tree = ttk.Treeview(TableMargin, columns=(col_names), height=35, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
   
   scrollbary.config(command=tree.yview)
   scrollbary.pack(side=RIGHT, fill=Y)
   scrollbarx.config(command=tree.xview)
   scrollbarx.pack(side=BOTTOM, fill=X)

   tree.column('#0', stretch=NO, minwidth=0, width=0)

   num = 0
   for i in col_names:
      tree.heading(num, text=i, anchor=W)
      tree.column(num, stretch=NO, minwidth=0, width=10)
      num += num

   tree.pack()

   # with open(csvfile) as f:
   #  reader = csv.DictReader(f, delimiter=',')
   #  for row in reader:
   #    1 = row['1']
   #    2 = row['2']
   #    3 = row['3']
   #    4 = row['4']
   #    tree.insert("", 0, values=(1,2,3,4))

# start window
win.mainloop()