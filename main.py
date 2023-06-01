import tetris
import settings
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
        "blitz_highscore": 0,
        "lines_highscore": 0,
        "zen_highscore": 0
    }
}

red = chalk.Chalk("red")
yellow = chalk.Chalk("yellow")
magenta = chalk.Chalk("magenta")
white = chalk.Chalk("white")

if not os.path.isfile("./config.json"):
    config_file = open("config.json", "w")
    config_file.write(json.dumps(default_config))
    config_file.close()
    
config_file = open("config.json", "r")
config_raw = config_file.read()
config = json.loads(config_raw)
config_file.close()

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
  _______ ______ _______ _____              _______ ______ _______ _____            
 |__   __|  ____|__   __|  __ \     /\     |__   __|  ____|__   __|  __ \     /\    
    | |  | |__     | |  | |__) |   /  \       | |  | |__     | |  | |__) |   /  \   
    | |  |  __|    | |  |  _  /   / /\ \      | |  |  __|    | |  |  _  /   / /\ \  
    | |  | |____   | |  | | \ \  / ____ \     | |  | |____   | |  | | \ \  / ____ \ 
    |_|  |______|  |_|  |_|  \_\/_/    \_\    |_|  |______|  |_|  |_|  \_\/_/    \_\\\n'''))
        
        print(chalk.bold(f"WELCOME!"))
        print(chalk.bold("(1) ") + yellow("Blitz", bold=True) + " - Highscore: " + str(config["user"]["blitz_highscore"]))
        print(chalk.bold("(2) ") + red("40 Lines", bold=True) + " - Highscore: " + str(config["user"]["lines_highscore"]) + 's')
        print(chalk.bold("(3) ") + magenta("Zen", bold=True) + " - Highscore: Level " + str(config["user"]["zen_highscore"]))
        print(chalk.bold("(4) ") + white("Settings", bold=True))
        print(chalk.bold("(5) ") + "Exit")
        choice = input("? ")
        if choice.isnumeric():
            if int(choice) > 0 and int(choice) < 6:
                if int(choice) == 1:
                    score = tetris.tetris(config["game"], 0)
                    if score > config['user']['blitz_highscore']:
                        config['user']['blitz_highscore'] = score
                elif int(choice) == 2:
                    lines_time = tetris.tetris(config["game"], 1)
                    if lines_time != 0 and (lines_time < config['user']['lines_highscore'] or config['user']['lines_highscore'] == 0):
                        config['user']['lines_highscore'] = lines_time
                elif int(choice) == 3:
                    level = tetris.tetris(config["game"], 2)
                    if level > config['user']['zen_highscore']:
                        config['user']['zen_highscore'] = level
                elif int(choice) == 4:
                    settings.settings()
                    config_file = open("config.json", "r")
                    config_raw = config_file.read()
                    config = json.loads(config_raw)
                    config_file.close()
                elif int(choice) == 5:
                    running = False
            config_raw = json.dumps(config)
            config_file = open("config.json", "w")
            config_file.write(config_raw)
            config_file.close()