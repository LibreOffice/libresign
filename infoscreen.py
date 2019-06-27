#!/usr/bin/python3
# fill the screen with a background + URL for playlist website +
# instructions on how to use this software
# this runs as a separate process

from multiprocessing import Process
import tkinter as tk

proc = None
bg_color = "#00A500"

class TKInfoScreen(tk.Frame):
    def __init__ (self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

    def setup (self, url):
        self.url_text = tk.Label(self.master)
        self.url_text["text"] = url
        self.url_text.configure(background=bg_color, foreground='white', font=("Helvetica", 30))
        self.url_text.place(relx='0.5', rely='0.5', anchor='center', height=50)

def info (url):
    root = tk.Tk()
    root.configure(background=bg_color)
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    app = TKInfoScreen(master=root)
    app.setup(url)
    app.mainloop()

def start_info (url):
    proc = Process(target=info, args=(url,))
    proc.start()
    # proc.join()

def stop_info ():
    if proc:
        proc.terminate()

