import tetris
import chalk
import pygame
import os
import json

pygame.init()

default_config = {
    "game": {
        "screen_width": 1000,
        "screen_height": 800,
        "fps_counter": True,
        "controls": {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "rotate_cw": pygame.K_UP,
            "rotate_ccw": pygame.K_z,
            "rotate_180": pygame.K_c,
            "hard_drop": pygame.K_SPACE,
            "soft_drop": pygame.K_DOWN,
            "hold": pygame.K_LSHIFT
        },
        "handling": {
            "ARR": 33,
            "DAS": 167,
            "DCD": 17,
            "SDF": 6
        }
    },
    "user": {
        "highscore": 0
    }
}

red = chalk.Chalk("red")
yellow = chalk.Chalk("yellow")
magenta = chalk.Chalk("magenta")
white = chalk.Chalk("white")

if not os.path.isfile("./config.json"):
    config_file = open("config.json", "w")
    config_file.write(json.dumps(default_config))
    
config_raw = open("config.json", "r").read()
config = json.loads(config_raw)

def clear():
    # checks for os and sends appropriate clear command
    if os.name == 'posix':
        os.system("clear")
    else:
        os.system("cls")

if __name__ == "__main__":
    running = True
    while running:
        clear()
        print(chalk.blue('''  
  _______ ______ _______ _____  _____  _____ 
 |__   __|  ____|__   __|  __ \|_   _|/ ____|
    | |  | |__     | |  | |__) | | | | (___  
    | |  |  __|    | |  |  _  /  | |  \___ \ 
    | |  | |____   | |  | | \ \ _| |_ ____) |
    |_|  |______|  |_|  |_|  \_\_____|_____/\n\n'''))
        
        print(chalk.bold(f"WELCOME!"))
        print(chalk.bold("(1) ") + yellow("Blitz", bold=True))
        print(chalk.bold("(2) ") + red("40 Lines", bold=True))
        print(chalk.bold("(3) ") + magenta("Zen", bold=True))
        print(chalk.bold("(4) ") + white("Settings", bold=True))
        choice = input("? ")
        
        if choice.isnumeric():
            if int(choice) > 0 and int(choice) < 5:
                if int(choice) == 1:
                    score = tetris.tetris(config["game"], 0)
                if int(choice) == 2:
                    time = tetris.tetris(config["game"], 1)
                if int(choice) == 3:
                    tetris.tetris(config["game"], 2)

        if score > config['user']['highscore']:
            config['user']['highscore'] = score
            open("config.json", "w").write(json.dumps(config))