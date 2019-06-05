#!/usr/bin/python3
# fill the screen with a background + URL for playlist website +
# instructions on how to use this software
# this runs as a separate process

from multiprocessing import Process
import tkinter as tk

proc = None

class TKInfoScreen(tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

    def setup (self, url):
        self.url_text = tk.Label(self)
        self.url_text["text"] = url
        self.url_text.pack(side="top")

def info (url):
    root = tk.Tk()
    app = TKInfoScreen(master=root)
    app.setup(url)
    app.mainloop()

def start_info (url):
    proc = Process(target=info, args=(url,))
    proc.start()
    proc.join()

def stop_info ():
    pass
    # if proc:
    #     proc.stop()

