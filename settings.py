from tkinter import *
from tkinter import ttk

def settings():
    # create window
    root = Tk()
    root.title("Tetra Tetra Settings")

    # create main frame
    mainframe = Frame(root, padx="10", pady="12")
    # add too main window
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    # fill extra space
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    title_text = Label(mainframe, text="Tetra Tetra Settings", font=("Arial", 20)).grid(row=0, column=0)
    
    # controls
    

    root.mainloop()

if __name__ == "__main__":
    settings()