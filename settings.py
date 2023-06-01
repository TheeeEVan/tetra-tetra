from tkinter import *
import pygame
import json

pygame.init()

font = pygame.font.Font("assets/fonts/Rubik-VariableFont_wght.ttf", 20)
press_a_key = font.render("Press any Key...", True, (255, 255, 255))
press_a_key_rect = press_a_key.get_rect()
press_a_key_rect.center = (100, 10)

def settings():

    def change_control(name):
        screen = pygame.display.set_mode((200, 25))
        running = True
        screen.blit(press_a_key, press_a_key_rect)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    config_new["game"]["controls"][name] = event.key
                    running = False
            pygame.display.flip()
        pygame.display.quit()
        update_all()
    
    def update_all():
        left_key.set(pygame.key.name(config_new["game"]["controls"]["left"]))
        right_key.set(pygame.key.name(config_new["game"]["controls"]["right"]))
        cw_key.set(pygame.key.name(config_new["game"]["controls"]["rotate_cw"]))
        ccw_key.set(pygame.key.name(config_new["game"]["controls"]["rotate_ccw"]))
        r180_key.set(pygame.key.name(config_new["game"]["controls"]["rotate_180"]))
        hard_key.set(pygame.key.name(config_new["game"]["controls"]["hard_drop"]))
        soft_key.set(pygame.key.name(config_new["game"]["controls"]["soft_drop"]))
        hold_key.set(pygame.key.name(config_new["game"]["controls"]["hold"]))
        config_new["game"]["handling"]["ARR"] = arr_value.get()
        config_new["game"]["handling"]["DAS"] = das_value.get()
        config_new["game"]["handling"]["DCD"] = dcd_value.get()
        config_new["game"]["handling"]["SDF"] = sdf_value.get()
        config_new["game"]["fps_counter"] = fps_value.get()

    def reset_scores():
        config_new["user"]["blitz_highscore"] = 0
        config_new["user"]["lines_highscore"] = 0
        config_new["user"]["zen_highscore"] = 0

    def apply():
        config_raw = json.dumps(config_new)
        config_file = open("config.json", "w")
        config_file.write(config_raw)
        config_file.close()
        root.destroy()

    # load config 
    config_file = open("config.json", "r")
    config_raw = config_file.read()
    config_file.close()
    config_new = json.loads(config_raw)

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
    left_key = StringVar()
    left_button = Button(mainframe, textvariable=left_key, command= lambda name="left": change_control(name), width="10").grid(row=2, column=1, sticky=(W))

    # right
    right_label = Label(mainframe, text="Right", font=("Arial", 11)).grid(row=3, column=0, sticky=(N,W))
    right_key = StringVar()
    right_button = Button(mainframe, textvariable=right_key, command= lambda name="right": change_control(name), width="10").grid(row=3, column=1, sticky=(W))

    # rotate cw
    cw_label = Label(mainframe, text="Rotate Clockwise", font=("Arial", 11)).grid(row=4, column=0, sticky=(N,W))
    cw_key = StringVar()
    cw_button = Button(mainframe, textvariable=cw_key, command= lambda name="rotate_cw": change_control(name), width="10").grid(row=4, column=1, sticky=(W))
    
    # rotate ccw
    ccw_label = Label(mainframe, text="Rotate Counter Clockwise", font=("Arial", 11)).grid(row=5, column=0, sticky=(N,W))
    ccw_key = StringVar()
    ccw_button = Button(mainframe, textvariable=ccw_key, command= lambda name="rotate_ccw": change_control(name), width="10").grid(row=5, column=1, sticky=(W))

    # rotate 180
    r180_label = Label(mainframe, text="Rotate 180", font=("Arial", 11)).grid(row=6, column=0, sticky=(N,W))
    r180_key = StringVar()
    r180_button = Button(mainframe, textvariable=r180_key, command= lambda name="rotate_180": change_control(name), width="10").grid(row=6, column=1, sticky=(W))

    # hard drop
    hard_label = Label(mainframe, text="Hard Drop", font=("Arial", 11)).grid(row=7, column=0, sticky=(N,W))
    hard_key = StringVar()
    hard_button = Button(mainframe, textvariable=hard_key, command= lambda name="hard_drop": change_control(name), width="10").grid(row=7, column=1, sticky=(W))


    # soft drop
    soft_label = Label(mainframe, text="Soft Drop", font=("Arial", 11)).grid(row=8, column=0, sticky=(N,W))
    soft_key = StringVar()
    soft_button = Button(mainframe, textvariable=soft_key, command= lambda name="soft_drop": change_control(name), width="10").grid(row=8, column=1, sticky=(W))

    # hold
    hold_label = Label(mainframe, text="Hold", font=("Arial", 11)).grid(row=9, column=0, sticky=(N,W))
    hold_key = StringVar()
    hold_button = Button(mainframe, textvariable=hold_key, command= lambda name="hold": change_control(name), width="10").grid(row=9, column=1, sticky=(W))

    # --- HANDLING ---
    handling_header = Label(mainframe, text="Handling", font=("Arial", 15)).grid(row=10,column=0,sticky=(N,W))

    # arr
    arr_label = Label(mainframe, text="ARR", font=("Arial", 11)).grid(row=11, column=0, sticky=(S,W))
    arr_value = IntVar()
    arr_value.set(config_new["game"]["handling"]["ARR"])
    arr_slider = Scale(mainframe, variable=arr_value, from_=83, to=0, orient=HORIZONTAL, command=lambda a: update_all()).grid(row=11, column=1)

    # das
    das_label = Label(mainframe, text="DAS", font=("Arial", 11)).grid(row=12, column=0, sticky=(S,W))
    das_value = IntVar()
    das_value.set(config_new["game"]["handling"]["DAS"])
    das_slider = Scale(mainframe, variable=das_value, from_=333, to=17, orient=HORIZONTAL, command=lambda a: update_all()).grid(row=12, column=1)

    # dcd
    dcd_label = Label(mainframe, text="DCD", font=("Arial", 11)).grid(row=13, column=0, sticky=(S,W))
    dcd_value = IntVar()
    dcd_value.set(config_new["game"]["handling"]["DCD"])
    dcd_slider = Scale(mainframe, variable=dcd_value, from_=333, to=0, orient=HORIZONTAL, command=lambda a: update_all()).grid(row=13, column=1)

    # sdf
    sdf_label = Label(mainframe, text="SDF", font=("Arial", 11)).grid(row=14, column=0, sticky=(S,W))
    sdf_value = IntVar()
    sdf_value.set(config_new["game"]["handling"]["SDF"])
    sdf_slider = Scale(mainframe, variable=sdf_value, from_=0, to=40, orient=HORIZONTAL, command=lambda a: update_all()).grid(row=14, column=1)

    # info
    sdf_info = Label(mainframe, text="SDF value of 0 is equivlent to instant soft drop").grid(row=15, column=0, columnspan=2)

    # -- OTHER -- 
    handling_header = Label(mainframe, text="Other", font=("Arial", 15)).grid(row=16,column=0,sticky=(N,W))

    fps_label = Label(mainframe, text="Show FPS", font=("Arial", 11)).grid(row=17, column=0, sticky=(S,W))
    fps_value = BooleanVar()
    fps_value.set(config_new["game"]["fps_counter"])
    fps_check = Checkbutton(mainframe, variable=fps_value, command=update_all).grid(row=17, column=1, sticky=(N,W))

    reset_label = Label(mainframe, text="Reset Highscores", font=("Arial", 11)).grid(row=18, column=0, sticky=(S,W))
    reset_button = Button(mainframe, text="Click Me", width=10, command=reset_scores).grid(row=18, column=1, sticky=(W))

    # -- EXIT --
    cancel_button = Button(mainframe, text="Cancel", width=10, command=root.destroy).grid(row=19,column=0, sticky=(W), pady=10)
    apply_button = Button(mainframe, text="Apply", width=10, command=apply).grid(row=19,column=1, sticky=(E), pady=10)

    update_all()
    root.mainloop()

if __name__ == "__main__":
    settings()