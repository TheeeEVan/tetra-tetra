# handles all IO and UI as well as score and timing

import pygame
import math
from events import *
from gamehandler import Game

def tetris(config, mode):
    # init
    pygame.init()

    # FONTS
    font_fps = pygame.font.Font('freesansbold.ttf', 15)
    text_font = pygame.font.Font('assets/fonts/Rubik-VariableFont_wght.ttf', 30)
    title_font = pygame.font.Font('assets/fonts/Rubik-VariableFont_wght.ttf', 50)
    text_font.bold = True
    score_font = pygame.font.Font('assets/fonts/VT323-Regular.ttf', 50)

    # COLORS
    BG = (20, 20, 20)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    # LEVEL SPEEDS (frames per row) - based off gameboy tetris
    speeds = [53, 49, 45, 41, 37, 33, 28, 22, 17, 11, 10, 9, 8, 7, 6, 6, 5, 5, 4, 4, 3]

    # PIECES
    # first one is none so we dont have to subtract one from piece id 
    # 1 - cyan
    # 2 - yellow
    # 3 - purple
    # 4 - green
    # 5 - red
    # 6 - blue
    # 7 - orange


    # setup screen
    screen = pygame.display.set_mode((config["screen_width"], config["screen_height"]))
    pygame.display.set_caption("Tetra Tetra")
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)
    # clock
    clock = pygame.time.Clock()
    # timers
    time_running = 0
    last_dt = 0
    lock_delay = 0
    move_reset = 0
    hard_drop_enabled_time = 0
    # score
    score = 0
    lines = 0
    level = 0
    # speeds
    drop_speed = speeds[level] / 60 * 1000
    soft_drop = False

    # handling
    das_time = 0
    arr_time = 0
    last_down = 0
    moving_left = False
    moving_right = False
    hard_drop_enabled = True

    # already held
    held = False

    # create game object
    game = Game(screen)

    # all pre rendered text
    next_text = text_font.render("NEXT", True, WHITE)
    hold_text = text_font.render("HOLD", True, WHITE)
    title_text = title_font.render("TETRIS", True, WHITE)
    title_rect = title_text.get_rect()
    title_rect.center = (500, 20)

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
        
        time_running += dt

        # add to time since last fall
        last_dt += dt

        # if piece cannot fall add to lock_delay
        if not game.can_fall():
            lock_delay += dt
        
        # time since last piece down
        if last_down:
            das_time += dt

        # set arr if using auto move
        if moving_left or moving_right:
            arr_time += dt
        
        # used for slight hard drop delay to avoid accidental hardrops
        if hard_drop_enabled == False:
            hard_drop_enabled_time += dt

        # if hardrop has been disabled for over 100ms enable it
        if hard_drop_enabled_time > 100:
            hard_drop_enabled = True
            hard_drop_enabled_time = 0

        # CONTROLS AND SCORING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # left
                if event.key == config["controls"]["left"]:
                    moving_right = False
                    das_time = 0
                    game.left()
                    last_down = 1
                    if move_reset < 15 and not game.can_fall():
                        lock_delay = 0
                        move_reset += 1
                # right
                elif event.key == config["controls"]["right"]:
                    moving_left = False
                    das_time = 0
                    game.right()
                    last_down = 2
                    if move_reset < 15 and not game.can_fall():
                        lock_delay = 0
                        move_reset += 1
                # rotate cw
                elif event.key == config["controls"]["rotate_cw"]:
                    game.rotate_cw()
                    if move_reset < 15 and not game.can_fall():
                        lock_delay = 0
                        move_reset += 1
                # rotate ccw
                elif event.key == config["controls"]["rotate_ccw"]:
                    game.rotate_ccw()
                    if move_reset < 15 and not game.can_fall():
                        lock_delay = 0
                        move_reset += 1
                # rotate 180
                elif event.key == config["controls"]["rotate_180"]:
                    game.rotate_180()
                    if move_reset < 15 and not game.can_fall():
                        lock_delay = 0
                        move_reset += 1
                # hard drop
                elif event.key == config["controls"]["hard_drop"]:
                    if hard_drop_enabled:
                        game.drop()
                        held = False
                        das_time = config["handling"]["DAS"] - config["handling"]["DCD"]
                # soft drop
                elif event.key == config["controls"]["soft_drop"]:
                    # checks if instant soft drop is on
                    if config["handling"]["SDF"] == 0:
                        game.drop_soft()
                        soft_drop = True
                    else:
                        soft_drop = True
                        drop_speed /= config["handling"]["SDF"]
                # hold
                elif event.key == config["controls"]["hold"]:
                    if not held:
                        game.hold_piece()
                        held = True
                        lock_delay = 0
                        move_reset = 0
            # these disable arr and soft drop
            elif event.type == pygame.KEYUP:
                # disable left arr
                if event.key == config["controls"]["left"]:
                    last_down = 0
                    moving_left = False
                    das_time = 0
                # disable right arr
                elif event.key == config["controls"]["right"]:
                    last_down = 0
                    moving_right = False
                    das_time = 0
                # disable soft drop
                elif event.key == config["controls"]["soft_drop"]:
                    if config["handling"]["SDF"] != 0:
                        drop_speed *= config["handling"]["SDF"]
                    soft_drop = False
            # SCORING EVENTS
            # blitz
            if mode == 0:
                if event.type == SINGLE_LINE:
                    score += 100 * (level + 1)
                elif event.type == DOUBLE_LINE:
                    score += 300 * (level + 1)
                elif event.type == TRIPLE_LINE:
                    score += 500 * (level + 1)
                elif event.type == TETRIS_LINE:
                    score += 800 * (level + 1)
                elif event.type == SPIN:
                    score += 400 * (level + 1)
                elif event.type == SINGLE_SPIN:
                    score += 800 * (level + 1)
                elif event.type == DOUBLE_SPIN:
                    score += 1200 * (level + 1)
                elif event.type == TRIPLE_SPIN:
                    score += 1600 * (level + 1)
                elif event.type == SINGLE_CLEAR:
                    score += 800 * (level + 1)
                elif event.type == DOUBLE_CLEAR:
                    score += 1200 * (level + 1)
                elif event.type == TRIPLE_CLEAR:
                    score += 1800 * (level + 1)
                elif event.type == TETRIS_CLEAR:
                    score += 2000 * (level + 1)
                elif event.type == SOFT_DROP_LINE:
                    score += 1
                elif event.type == HARD_DROP_LINE:
                    score += 2
                elif event.type == LINE:
                    lines += 1
                    level = math.floor(lines / 10)
                    drop_speed = speeds[level] / 60 * 1000
            # 40 lines
            if mode == 1:
                # our score counter will show the amount of lines you've cleared
                if event.type == LINE:
                    lines += 1
                    score += 1
                    level = math.floor(lines / 10)
                    drop_speed = speeds[level] / 60 * 1000
            # zen
            if mode == 2:
                # just show the level
                if event.type == LINE:
                    lines += 1
                    level = math.floor(lines / 10)
                    score = level
                    drop_speed = speeds[level] / 60 * 1000
            # if gameover close
            if event.type == GAMEOVER:
                running = False

        # handles instant hard drops
        if soft_drop and config['handling']['SDF'] == 0:
            game.drop_soft()

        # drop according to drop_speed
        if last_dt >= drop_speed:
            if soft_drop and mode == "0":
                score += 1
            game.fall()
            last_dt = 0

        # this is arr
        # automatic repeat is just when pieces move automatically after holding key
        # das is used because das (delay auto shift) is how long after a key is pressed until it begins rotating
        if das_time > config["handling"]["DAS"] and not moving_left and not moving_right:
            if last_down == 1:
                if config["handling"]["ARR"] > 0:
                    moving_left = True
                else:
                    for i in range(10):
                        game.left()
            elif last_down == 2:
                if config["handling"]["ARR"] > 0:
                    moving_right = True
                else:
                    for i in range(10):
                        game.right()
        
        # this makes arr actualy move
        if arr_time > config["handling"]["ARR"]:
            arr_time = 0
            if moving_left:
                game.left()
            if moving_right:
                game.right()

        # lock piece if over lock delay
        if lock_delay >= 500:
            hard_drop_enabled = False
            game.lock_piece()
            held = 0
            das_time = config["handling"]["DAS"] - config["handling"]["DCD"]
            move_reset = 0
            lock_delay = 0
        # if over move reset and cant fall lock right away
        elif move_reset == 15 and not game.can_fall():
            hard_drop_enabled = False
            game.lock_piece()
            held = 0
            das_time = config["handling"]["DAS"] - config["handling"]["DCD"]
            move_reset = 0
            lock_delay = 0

        # title text
        screen.blit(next_text, (750, 40))
        screen.blit(hold_text, (200, 40))
        screen.blit(title_text, title_rect)

        # score text
        score_text = score_font.render(str(score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.center = (500, 750)
        screen.blit(score_text, score_rect)

        # DRAW
        # draw the grid
        game.draw()

        # if playing blitz and over 2min end
        if mode == 0 and time_running > 120000:
            running = False

        # if 40 lines have cleared in 40 lindes mode end
        if mode == 1 and score >= 40:
            running = False

        # check if fps counter is turned on
        if config["fps_counter"]:
            fps_counter()
        # update display
        pygame.display.update()

    pygame.quit()
    # return score for blitz
    if mode == 0:
        return score
    # reuturn lines cleared if 40 lines 
    elif mode == 1:
        # only if 40 lines were finished
        if score >= 40:
            return math.ceil(time_running / 1000)
        else:
            return 0
    # if zen return level
    elif mode == 2:
        return level