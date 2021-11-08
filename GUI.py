import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

win= Tk()

#resize window
win.geometry("700x600")

#this is what happens when you click the import button
def import_box(event=None):
   filename = filedialog.askopenfilename() #unsure if this can do multiple files
   print('Selected:', filename)
   output.configure(state='normal')
   output.insert(tk.END, 'Selected file: ')
   output.insert(tk.END, filename)
   output.insert(tk.END, '\n')
   output.see(tk.END)
   output.configure(state='disabled')
   #call to add file to queue

#this is what happens when you click the clear button
def clear_queue(event=None):
   print('queue clear event')
   output.configure(state='normal')
   output.insert(tk.END, 'Queue Cleared (theres no queue yet)\n')
   output.see(tk.END)
   output.configure(state='disabled')
   #call clear queue

#this is what happens when you click the GO button
def start(event=None):
   print('start process')
   output.configure(state='normal')
   output.insert(tk.END, 'Analyzing... (actually its not)\n')
   output.see(tk.END)
   output.configure(state='disabled')
   #call the script

#create label
Label(win, text= "File fuckin test thing").pack(pady= 10)

#create buttons
ttk.Button(win, text= "Import PCAP Files", command=import_box).pack(pady= 10)
ttk.Button(win, text= "Clear Queue", command=clear_queue).pack(pady= 10)
ttk.Button(win, text= "Analyze", command=start).pack(pady= 10)

#output window
output = Text(win, state = 'disabled', width=80, height=60)
output.pack(pady=20)

win.mainloop()
