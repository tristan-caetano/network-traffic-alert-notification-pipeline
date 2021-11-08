import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

win= Tk()

#resize window
win.geometry("1200x800")
win.title("cool gui for cool boys")

#this is what happens when you click the import button
def import_box(event=None):
   filename = filedialog.askopenfilename() #unsure if this can do multiple files
   print('Added:', filename)
   lst.append(filename)
   queue.configure(state='normal')
   queue.insert(tk.END, filename)
   queue.insert(tk.END, '\n')
   queue.see(tk.END)
   queue.configure(state='disabled')
   print(lst)

#this is what happens when you click the clear button
def clear_queue(event=None):
   print('queue clear event')
   queue.configure(state='normal')
   queue.delete(1.0, END)
   queue.configure(state='disabled')
   lst.clear()

#this is what happens when you click the GO button
def start(event=None):
   print('start process')
   output.configure(state='normal')
   output.insert(tk.END, 'Starting process...\n')
   output.see(tk.END)
   output.configure(state='disabled')
   #call the script using lst as the file queue

#create labels
Label(win, text= "WORLDS GREATEST GUI").pack(pady= 10)
Label(win, text= "QUEUE:").place(x=50, y=184)
Label(win, text= "OUTPUT:").place(x=400, y=40)

#create buttons
ttk.Button(win, text= "Import PCAP Files", command=import_box).place(x=50, y=40)
ttk.Button(win, text= "Clear Queue", command=clear_queue).place(x=50, y=80)
ttk.Button(win, text= "Analyze", command=start).place(x=50, y=120)

#file queue
queue = Text(win, state = 'disabled', width=40, height=31)
queue.place(x=50, y=204)

#output window
output = Text(win, state = 'disabled', width=90, height=40)
output.place(x=400, y=60)

#initialize queue list
lst = []

win.mainloop()
