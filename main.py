# Import modules
from tkinter import *
import tkinter as ttk
import screeninfo

class app:
    def __init__(self):
        self.set_window()
        
    def set_window(self):
        # Get the resolution of the current screen
        windowW = screeninfo.screeninfo.get_monitors()[0].width
        windowH = screeninfo.screeninfo.get_monitors()[0].height
        self.root = Tk()
        self.root.title("revision")
        self.root.geometry(f"{windowW}x{windowH}")
        self.frame = ttk.Frame(self.root)
        
    def run(self):
        self.root.mainloop()
    
if __name__ == "__main__":
    a = app()
    a.run()