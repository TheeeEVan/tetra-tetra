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

    # create title_text
    title_text = Label(mainframe, text="Tetra Tetra Settings", font=("Arial", 20)).grid(row=0, column=0, columnspan=2,sticky=(N,W))
    
    # --- CONTROLS ---
    controls_header = Label(mainframe, text="Controls", font=("Arial", 15)).grid(row=1,column=0,sticky=(N,W))

    # left
    left_label = Label(mainframe, text="Left", font=("Arial", 11)).grid(row=2, column=0, sticky=(N,W))
    left_button = Button(mainframe, text="left", command= lambda name="left": change_control(name), width="10").grid(row=2, column=1, sticky=(W))

    # right
    right_label = Label(mainframe, text="Right", font=("Arial", 11)).grid(row=3, column=0, sticky=(N,W))
    right_button = Button(mainframe, text="right", command= lambda name="right": change_control(name), width="10").grid(row=3, column=1, sticky=(W))

    # rotate cw
    cw_label = Label(mainframe, text="Rotate Clockwise", font=("Arial", 11)).grid(row=4, column=0, sticky=(N,W))
    cw_button = Button(mainframe, text="up", command= lambda name="rotate_cw": change_control(name), width="10").grid(row=4, column=1, sticky=(W))
    
    # rotate ccw
    ccw_label = Label(mainframe, text="Rotate Counter Clockwise", font=("Arial", 11)).grid(row=5, column=0, sticky=(N,W))
    ccw_button = Button(mainframe, text="z", command= lambda name="rotate_ccw": change_control(name), width="10").grid(row=5, column=1, sticky=(W))

    # rotate 180
    r180_label = Label(mainframe, text="Rotate 180", font=("Arial", 11)).grid(row=6, column=0, sticky=(N,W))
    r180_button = Button(mainframe, text="c", command= lambda name="rotate_180": change_control(name), width="10").grid(row=6, column=1, sticky=(W))

    # hard drop
    hard_label = Label(mainframe, text="Hard Drop", font=("Arial", 11)).grid(row=7, column=0, sticky=(N,W))
    hard_button = Button(mainframe, text="space", command= lambda name="hard_drop": change_control(name), width="10").grid(row=7, column=1, sticky=(W))


    # soft drop
    soft_label = Label(mainframe, text="Soft Drop", font=("Arial", 11)).grid(row=8, column=0, sticky=(N,W))
    soft_button = Button(mainframe, text="down", command= lambda name="soft_drop": change_control(name), width="10").grid(row=8, column=1, sticky=(W))

    # hold
    hold_label = Label(mainframe, text="Hold", font=("Arial", 11)).grid(row=9, column=0, sticky=(N,W))
    hold_button = Button(mainframe, text="shift", command= lambda name="hold": change_control(name), width="10").grid(row=9, column=1, sticky=(W))

    # --- HANDLING ---
    handling_header = Label(mainframe, text="Handling", font=("Arial", 15)).grid(row=10,column=0,sticky=(N,W))

    # arr
    arr_label = Label(mainframe, text="ARR", font=("Arial", 11)).grid(row=11, column=0, sticky=(S,W))
    arr_slider = Scale(mainframe, from_=83, to=0, orient=HORIZONTAL).grid(row=11, column=1)

    # das
    das_label = Label(mainframe, text="DAS", font=("Arial", 11)).grid(row=12, column=0, sticky=(S,W))
    das_slider = Scale(mainframe, from_=333, to=17, orient=HORIZONTAL).grid(row=12, column=1)

    # dcd
    dcd_label = Label(mainframe, text="DCD", font=("Arial", 11)).grid(row=13, column=0, sticky=(S,W))
    dcd_slider = Scale(mainframe, from_=333, to=0, orient=HORIZONTAL).grid(row=13, column=1)

    # sdf
    sdf_label = Label(mainframe, text="SDF", font=("Arial", 11)).grid(row=14, column=0, sticky=(S,W))
    sdf_slider = Scale(mainframe, from_=5, to=41, orient=HORIZONTAL).grid(row=14, column=1)

    # info
    sdf_info = Label(mainframe, text="SDF value of 41 is equivlent to instant drop").grid(row=15, column=0, columnspan=2)

    # -- OTHER -- 
    handling_header = Label(mainframe, text="Other", font=("Arial", 15)).grid(row=16,column=0,sticky=(N,W))

    fps_label = Label(mainframe, text="Show FPS", font=("Arial", 11)).grid(row=17, column=0, sticky=(S,W))
    fps_check = Checkbutton(mainframe).grid(row=17, column=1, sticky=(N,W))

    reset_label = Label(mainframe, text="Reset Highscores", font=("Arial", 11)).grid(row=18, column=0, sticky=(S,W))
    reset_button = Button(mainframe, text="Click Me", width=10).grid(row=18, column=1, sticky=(W))

    # -- EXIT --
    cancel_button = Button(mainframe, text="Cancel", width=10).grid(row=19,column=0, sticky=(W), pady=10)
    apply_button = Button(mainframe, text="Apply", width=10).grid(row=19,column=1, sticky=(E), pady=10)

    root.mainloop()

def change_control(name):
    print(f"Change {name}")

if __name__ == "__main__":
    settings()