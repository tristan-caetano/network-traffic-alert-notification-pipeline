import tkinter as tk
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

# if os.environ.get('DISPLAY','') == '':
#     print('no display found. Using :0.0')
#     os.environ.__setitem__('DISPLAY', ':0.0')

win = tk.Tk()

#resize window
#win.geometry("700x350")

#this is what happens when you click the import button
def import_box(event=None):
   filename = filedialog.askopenfilename() #unsure if this can do multiple files
   print('Selected:', filename)#replace this with adding file(s) to queue

#this is what happens when you click the clear button
def clear_queue(event=None):
   print('queue clear event')#replace this

#this is what happens when you click the GO button
def start(event=None):
   print('start process')#call the analyze script

#create label
Label(win, text= "File fuckin test thing").pack(pady= 30)

#create buttons
ttk.Button(win, text= "Import PCAP Files", command=import_box).pack(pady= 20)
ttk.Button(win, text= "Clear Queue", command=clear_queue).pack(pady= 20)
ttk.Button(win, text= "Analyze", command=start).pack(pady= 20)

#create output textbox
# output = tk.Text(win, width = 25, height = 50)
# output.grid(row = 1, column = 0, columnspan = 50)
#to clear the output window -> output.delete(1.0,"") or something like that???
#to add to the output window -> output.insert("blhablahblahb") i think???

win.mainloop()