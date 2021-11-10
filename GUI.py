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

win= Tk()

# Resize window
win.geometry("1200x800")
win.title("cool gui for cool boys")

# This is what happens when you click the import button.
def import_box(event=None):
   global filename
   filename = filedialog.askopenfilename()
   print('Added:', filename)
   lst.append(filename)
   queue.configure(state='normal')
   queue.insert(tk.END, filename)
   queue.insert(tk.END, '\n')
   queue.see(tk.END)
   queue.configure(state='disabled')
   print(lst)

def import_box2(event=None):
   global filenameCSV
   filenameCSV = filedialog.askopenfilename()
   filenameCSV  = os.path.basename(filenameCSV)
   output.configure(state='normal')
   output.delete(1.0, END)

   # The if-statement and else-statement detects if the file is a CSV or not.
   my_str = filenameCSV[-4:]
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

# This is what happens when you click the clear button.
def clear_queue(event=None):
   print('queue clear event')
   queue.configure(state='normal')
   queue.delete(1.0, END)
   queue.configure(state='disabled')
   lst.clear()

# This is what happens when you click the GO button.
def start(event=None):
   print('start conversion')
   output.configure(state='normal')
   output.insert(tk.END, 'Starting Conversion...\n')
   output.see(tk.END)
   output.configure(state='disabled')
   cv.convert(output, filename)
   # Call the conversion script

# This is what happens when you click the CREATE TEST SET
def create_set(event=None):
   print('start create test set')
   output.configure(state='normal')
   output.insert(tk.END, 'Creating Test Set...\n')
   output.see(tk.END)
   output.configure(state='disabled')
   print("Running...: ", filenameCSV)
   print(type(filenameCSV))
   cts.digest_file(filenameCSV, output)
   # Call the script using filenameCSV

# Create labels
Label(win, text= "WORLDS GREATEST GUI").pack(pady= 10)
Label(win, text= "QUEUE:").place(x=50, y=184)
Label(win, text= "OUTPUT:").place(x=400, y=40)

# Create buttons
ttk.Button(win, text= "Import PCAP", command=import_box).place(x=50, y=40)
ttk.Button(win, text= "Clear Queue", command=clear_queue).place(x=50, y=80)
ttk.Button(win, text= "Convert to CSV", command=start).place(x=50, y=120)
ttk.Button(win, text= "Import CSV", command=import_box2).place(x=150, y=40)
ttk.Button(win, text= "Create Test Set", command=create_set).place(x=150, y=80)

# File queue
queue = Text(win, state = 'disabled', width=40, height=31)
queue.place(x=50, y=204)

# Output window
output = Text(win, state = 'disabled', width=90, height=40)
output.place(x=400, y=60)

# Initialize queue list
lst = []

win.mainloop()


#output.configure(state='normal')
#output.insert(tk.END, 'HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHHAHAHA')
#output.see(tk.END)
#output.configure(state='disabled')