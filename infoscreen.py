#!/usr/bin/python3
# fill the screen with a background + URL for playlist website +
# instructions on how to use this software
# this runs as a separate process

from multiprocessing import Process
import tkinter as tk

class TKInfoScreen(tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.setup()

    def setup (self):
        self.hi = tk.Button(self)
        self.hi["text"] = "hello ppl\n"
        self.hi.pack(side="top")

def info():
    root = tk.Tk()
    app = TKInfoScreen(master=root)
    app.mainloop()

def start_info():
    p = Process(target=info, args=())
    p.start()
    p.join()

