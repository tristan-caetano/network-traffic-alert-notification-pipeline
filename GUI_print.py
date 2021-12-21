# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Function that makes printing to the GUI output simple and clean

#  ---------------  Libraries  ---------------
import tkinter as tk

def print(output, text):
    output.configure(state='normal')
    output.insert(tk.END, text)
    output.see(tk.END)
    output.configure(state='disabled')
    output.update()
    