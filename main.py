import pygame
import math
from enum import Enum

# init pygame
pygame.init()

# config
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

# create surface
screen = pygame.display.set_mode((config["screen_width"], config["screen_height"]))

# start clock
clock = pygame.time.Clock()

# all fonts
class Fonts(Enum):
    FPS = pygame.font.Font('freesansbold.ttf', 30)


class Colors(Enum):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

# fps counter
def fps_counter():
    # get current fps
    fps = str(math.floor(clock.get_fps()))
    # render text
    text = Fonts.FPS.value.render(fps, True, Colors.GREEN.value)
    # draw on screen
    screen.blit(text, (0, 0))

# game loop
running = True
while running:
    # limit to 60 fps and assign deltatime
    dt = clock.tick(60)

    screen.fill((0,0,0))
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == config["controls"]["left"]:
                print("left")
            if event.key == config["controls"]["right"]:
                print("right")
            if event.key == config["controls"]["rotate_cw"]:
                print("rotate_cw")
            if event.key == config["controls"]["rotate_ccw"]:
                print("rotate_ccw")
            if event.key == config["controls"]["rotate_180"]:
                print("rotate_180")
            if event.key == config["controls"]["hard_drop"]:
                print("hard_drop")
            if event.key == config["controls"]["soft_drop"]:
                print("soft_drop")
            if event.key == config["controls"]["hold"]:
                print("hold")

    # check if fps counter is turned on
    if config["fps_counter"]:
        fps_counter()
    # update display
    pygame.display.update()