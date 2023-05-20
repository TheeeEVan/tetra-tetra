import pygame
import math
from game import Game
from enum import Enum

# init
pygame.init()

# CONFIG
# TODO: Load this from a json to allow changes to the file
config = {
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
    }
}

# FONTS
font_fps = pygame.font.Font('freesansbold.ttf', 15)
text_font = pygame.font.Font('fonts/Rubik-VariableFont_wght.ttf', 30)
text_font.bold = True


# COLORS
BG = (20, 20, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# PIECES
# first one is none so we dont have to subtract one from piece id 
# 1 - cyan
# 2 - yellow
# 3 - purple
# 4 - green
# 5 - red
# 6 - blue
# 7 - orange
piece_sprites = [None, pygame.image.load("assets/pieces/cyan.png"), pygame.image.load("assets/pieces/yellow.png"), pygame.image.load("assets/pieces/purple.png"), pygame.image.load("assets/pieces/green.png"), pygame.image.load("assets/pieces/red.png"), pygame.image.load("assets/pieces/blue.png"), pygame.image.load("assets/pieces/orange.png"), ]


# setup screen
screen = pygame.display.set_mode((config["screen_width"], config["screen_height"]))
clock = pygame.time.Clock()
last_dt = 0
drop_speed = 1000

# create game object
game = Game()

# fps counter
def fps_counter():
    # get current fps
    fps = str(math.floor(clock.get_fps()))
    # render text
    text = font_fps.render(fps, True, GREEN)
    # draw on screen
    screen.blit(text, (10, 10))

# game loop
running = True
while running:
    # limit to 60 fps and assign deltatime
    dt = clock.tick(60)
    # empty screen
    screen.fill(BG)
    last_dt += dt

    # every second drop
    if last_dt >= drop_speed:
        game.fall()
        last_dt = 0

    # CONTROLS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == config["controls"]["left"]:
                print("left")
                game.left()
            if event.key == config["controls"]["right"]:
                print("right")
                game.right()
            if event.key == config["controls"]["rotate_cw"]:
                print("rotate_cw")
            if event.key == config["controls"]["rotate_ccw"]:
                print("rotate_ccw")
            if event.key == config["controls"]["rotate_180"]:
                print("rotate_180")
            if event.key == config["controls"]["hard_drop"]:
                print("hard_drop")
                game.drop()
            if event.key == config["controls"]["soft_drop"]:
                print("soft_drop")
                drop_speed /= 10
            if event.key == config["controls"]["hold"]:
                print("hold")
        if event.type == pygame.KEYUP:
            if event.key == config["controls"]["left"]:
                print("left up")
            if event.key == config["controls"]["right"]:
                print("right up")
            if event.key == config["controls"]["soft_drop"]:
                print("soft_drop up")
                drop_speed *= 10

    # DRAW
    # draw the grid
    screen.blit(game.grid_sprite, (350, 100))

    # draw all pieces
    for row in range(22):
        for cell in range(10):
            if game.grid[row][cell][0] > 0:
                screen.blit(piece_sprites[game.grid[row][cell][0]], (cell*30+355, (19-row)*30+105))

    # draw nexts
    for row in range(14):
        for cell in range(4):
            if game.next_grid[row][cell] > 0:
                screen.blit(piece_sprites[game.next_grid[row][cell]], (cell*30+750, row*30+105))

    # all text
    next_text = text_font.render("NEXT", True, WHITE)
    screen.blit(next_text, (750, 40))

    # check if fps counter is turned on
    if config["fps_counter"]:
        fps_counter()
    # update display
    pygame.display.update()