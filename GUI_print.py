import tkinter as tk

def print(output, text):
    output.configure(state='normal')
    output.insert(tk.END, text)
    output.see(tk.END)
    output.configure(state='disabled')
    output.update()
    