# keeps track of the board and handles the result of most input

import pygame
import random
from events import *

class Game:
    def __init__(self, screen):
        # PIECES
        # 1 - I - cyan
        # 2 - O - yellow
        # 3 - T - purple
        # 4 - S - green
        # 5 - Z - red
        # 6 - J - blue
        # 7 - L - orange

        # keep the screen idk :(
        self.screen = screen

        # load sprites
        self.grid_sprite = pygame.image.load("assets/grid.png")
        self.piece_sprites = [None, pygame.image.load("assets/pieces/cyan.png"), pygame.image.load("assets/pieces/yellow.png"), pygame.image.load("assets/pieces/purple.png"), pygame.image.load("assets/pieces/green.png"), pygame.image.load("assets/pieces/red.png"), pygame.image.load("assets/pieces/blue.png"), pygame.image.load("assets/pieces/orange.png"), ]
        self.ghost_sprite = pygame.image.load("assets/pieces/ghost.png")
        
        # generate board
        self.board = []
        for i in range(40):
            self.board.append([])
            for j in range(10):
                self.board[i].append(0)

        self.pieces = [
            # I
            [
                [0,0,0,0],
                [1,1,1,1],
                [0,0,0,0],
                [0,0,0,0]
            ],
            # O
            [
                [0,2,2,0],
                [0,2,2,0]
            ],
            # T
            [
                [0,3,0],
                [3,3,3],
                [0,0,0]
            ],
            # S
            [
                [0,4,4],
                [4,4,0],
                [0,0,0]
            ],
            # Z
            [
                [5,5,0],
                [0,5,5],
                [0,0,0]
            ],
            # J
            [
                [6,0,0],
                [6,6,6],
                [0,0,0]
            ],
            # L
            [
                [0,0,7],
                [7,7,7],
                [0,0,0]
            ]
        ]

        # these are the offsets for the center rotation point that the rotation system will attempt before cancelling rotation
        # [90 or 180][I or non-I (only for 90)][(original rotation, desired rotation)]
        self.kick_table = {
            "90": {
                "non-I": {
                    (0, 1): [(-1, 0), (-1, 1), (0, -2), (-1, -2)],
                    (1, 0): [(1, 0), (1, -1), (0, 2), (1, 2)],
                    (1, 2): [(1, 0), (1, -1), (0, 2), (1, 2)],
                    (2, 1): [(-1, 0), (-1, 1), (0, -2), (-1, -2)],
                    (2, 3): [(1, 0), (1, 1), (0, -2), (1, -2)],
                    (3, 2): [(-1, 0), (-1, -1), (0, 2), (-1, 2)],
                    (3, 0): [(-1, 0), (-1, -1), (0, 2), (-1, 2)],
                    (0, 3): [(1, 0), (1, 1), (0, -2), (1, -2)]
                },

                "I": {
                    (0, 1): [(-2, 0), (1, 0), (-2, -1), (1, 2)],
                    (1, 0): [(2, 0), (-1, 0), (2, 1), (-1, -2)],
                    (1, 2): [(-1, 0), (2, 0), (-1, 2), (2, -1)],
                    (2, 1): [(1, 0), (-2, 0), (1, -2), (-2, 1)],
                    (2, 3): [(2, 0), (-1, 0), (2, 1), (-1, -2)],
                    (3, 2): [(-2, 0), (1, 0), (-2, -1), (1, 2)],
                    (3, 0): [(1, 0), (-2, 0), (1, -2), (-2, 1)],
                    (0, 3): [(-1, 0), (2, 0), (-1, 2), (2, -1)]
                }
            },
            "180": {
                (0, 2): [(0, 1), (1, 1), (-1, 1), (1, 0), (-1, 0)],
                (2, 0): [(0, -1), (-1, -1), (1, -1), (-1, 0), (1, 0)],
                (1, 3): [(1, 0), (1, 2), (1, 1), (0, 2), (0, 1)],
                (3, 1): [(-1, 0), (-1, 2), (-1, 1), (0, 2), (0, 1)]
            }
        }

        # generate first two bags
        self.next_pieces = self.generate_bag() + self.generate_bag()
        # increments everytime piece spawns, once 7 pieces add another bag
        self.spawns = 0

        self.current_piece = 0
        self.current_id = 0

        self.spawn_piece(self.next_pieces.pop(0))

        self.current_x = 3
        self.current_y = 21
        
        self.current_rotation = 0
        self.temp_rotation = 0

        # tspin detection stat
        self.last_move_was_rotate = False

        # stores id of held piece
        self.hold_id = 0
    # draws the game
    def draw(self):
        # draws grid sprite
        self.screen.blit(self.grid_sprite, (350, 100))

        # this is some scary code im not too sure what ive made but it works
        # draw board pieces
        # every row below 22
        for row in range(22):
            # every cell
            for cell in range(10):
                # if not empty
                if self.board[row][cell] > 0:
                    # draw correct piece and in the right spot
                    self.screen.blit(self.piece_sprites[self.board[row][cell]], (cell*30+355, (19-row)*30+105))

        # draw ghost
        ghost_y = self.get_ghost()
        for row in range(len(self.current_piece)):
            for cell in range(len(self.current_piece[0])):
                if self.current_piece[row][cell] > 0:
                    self.screen.blit(self.ghost_sprite, ((cell + self.current_x)*30+355, (19-(ghost_y - row))*30+105))

        # draw falling piece
        for row in range(len(self.current_piece)):
            for cell in range(len(self.current_piece[0])):
                if self.current_piece[row][cell] > 0:
                    self.screen.blit(self.piece_sprites[self.current_id], ((cell + self.current_x)*30+355, (19-(self.current_y - row))*30+105))

        # draw next pieces
        for piece in range(5):
            # the I piece fits weird so i have to do it differently
            if self.next_pieces[piece] == 1:
                for row in range(3):
                    for cell in range(4):
                        if self.pieces[self.next_pieces[piece] - 1][row][cell] > 0:
                            self.screen.blit(self.piece_sprites[self.next_pieces[piece]], (cell*30+750, piece*100+row*30+105))
            # same with square
            elif self.next_pieces[piece] == 2:
                for row in range(2):
                    for cell in range(3):
                        if self.pieces[self.next_pieces[piece] - 1][row][cell] > 0:
                            self.screen.blit(self.piece_sprites[self.next_pieces[piece]], (cell*30+750, piece*100+row*30+105))
            # all the other normal pieces
            else:
                for row in range(3):
                    for cell in range(3):
                        if self.pieces[self.next_pieces[piece] - 1][row][cell] > 0:
                            self.screen.blit(self.piece_sprites[self.next_pieces[piece]], (cell*30+750, piece*100+row*30+105))

        # draw held piece
        if self.hold_id > 0:
            for row in range(len(self.pieces[self.hold_id - 1])):
                for col in range(len(self.pieces[self.hold_id - 1][0])):
                    if self.pieces[self.hold_id - 1][row][col] > 0:
                        self.screen.blit(self.piece_sprites[self.hold_id], (col*30+200, row*30+105))

    # generates next piece bag
    # no one believes this is how it works: https://tetris.fandom.com/wiki/Random_Generator
    def generate_bag(self):
        # this is the bag
        pieces = [1, 2, 3, 4, 5, 6, 7]
        # shuffle the bag
        random.shuffle(pieces)
        # return the bag
        return pieces
    
    # just check if a piece can spawn
    def can_spawn(self, piece):
        # get the piece we need to sapwn
        test_piece = self.pieces[piece - 1]

        # loop through the piece and see if any square it needs to spawn is occupied
        for y in range(len(test_piece)):
            for x in range(len(test_piece[y])):
                if test_piece[y][x] > 0:
                    # if it is occupied just return false
                    if self.board[21- y][3 + x] != 0:
                        return False
        return True
    
    # finds where the ghost should be
    def get_ghost(self):
        # ghost y is the height the ghost is rendered at
        ghost_y = self.current_y

        # just keep moving the ghost down until it hits something
        while not self.intersecting(self.current_x, ghost_y):
            ghost_y -= 1

        # return ghost y (add 1 cause it hit something on the last sutraction)
        return ghost_y + 1

    # spawns specified piece
    def spawn_piece(self, piece):
        if self.can_spawn(piece):
            # add one to spawns
            self.spawns += 1

            # if seven pieces have spawned generate next bag
            if self.spawns == 7:
                self.next_pieces += self.generate_bag()
                self.spawns = 0

            # set currnet x and y to spawn
            self.current_x = 3
            self.current_y = 21
            # set piece to new piece
            self.current_piece = self.pieces[piece - 1]
            self.current_id = piece
            self.current_rotation = 0
        else:
            pygame.event.post(EVENT_GAMEOVER)

    # add piece to board to lock in place
    def lock_piece(self):
        # detect tspin
        tspin = False
    
        # ensure it's a T, ensure rotated last, ensure locked
        if self.current_id == 3 and self.last_move_was_rotate and not self.can_fall() and self.intersecting(self.current_x + 1, self.current_y) and self.intersecting(self.current_x - 1, self.current_y):
            if sum([self.board[self.current_y][self.current_x] > 0, self.board[self.current_y - 2][self.current_x] > 0, self.board[self.current_y][self.current_x + 2] > 0, self.board[self.current_y - 2][self.current_x + 2] > 0]) >= 3:
                tspin = True

        # go through all parts of the piece
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                # if part of the piece
                if self.current_piece[y][x] > 0:
                    # add to board using current id
                    self.board[self.current_y - y][self.current_x + x] = self.current_id
        
        lines = 0

        # clear lines
        for line in range(39, -1, -1):
            if 0 not in self.board[line]:
                lines += 1
                pygame.event.post(EVENT_LINE)
                for i in range(line, 39):
                    self.board[i] = self.board[i + 1]
                    self.board[i + 1] = [0,0,0,0,0,0,0,0,0,0]

        # send proper event based on what happened
        if lines == 1 and self.board[0] == [0,0,0,0,0,0,0,0,0,0]:
            pygame.event.post(EVENT_SINGLE_CLEAR)
        elif lines == 2 and self.board[0] == [0,0,0,0,0,0,0,0,0,0]:
            pygame.event.post(EVENT_DOUBLE_CLEAR)
        elif lines == 3 and self.board[0] == [0,0,0,0,0,0,0,0,0,0]:
            pygame.event.post(EVENT_TRIPLE_CLEAR)
        elif lines == 4 and self.board[0] == [0,0,0,0,0,0,0,0,0,0]:
            pygame.event.post(EVENT_TETRIS_CLEAR)
        elif lines == 1 and tspin:
            pygame.event.post(EVENT_SINGLE_SPIN)
        elif lines == 2 and tspin:
            pygame.event.post(EVENT_DOUBLE_SPIN)
        elif lines == 3 and tspin:
            pygame.event.post(EVENT_TRIPLE_SPIN)
        elif lines == 1:
            pygame.event.post(EVENT_SINGLE_LINE)
        elif lines == 2:
            pygame.event.post(EVENT_DOUBLE_LINE)
        elif lines == 3:
            pygame.event.post(EVENT_TRIPLE_LINE)
        elif lines == 4:
            pygame.event.post(EVENT_TETRIS_LINE)
        elif tspin:
            pygame.event.post(EVENT_SPIN)

        # now that line is gone send the next piece
        self.spawn_piece(self.next_pieces.pop(0))

    # returns bool stating whether the current piece can fall again
    def can_fall(self):
        # go through all parts of the piece
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                # if part of the piece
                if self.current_piece[y][x] > 0:
                    # check if there is blocks below it or if it is at the bottom of the board
                    if self.board[self.current_y - y - 1][self.current_x + x] > 0 or self.current_y - y < 1:
                        return False
        return True

    # causes a piece to fall one row
    def fall(self):
        if self.can_fall():
            self.current_y -= 1
    
    # drops a piece instantly
    def drop(self):
        # continue falling until piece hits something and lock
        while self.can_fall():
            pygame.event.post(EVENT_HARD_DROP_LINE)
            self.fall()
        self.lock_piece()

    # drops a piece instantly
    def drop_soft(self):
        # continue falling until piece hits something and lock
        while self.can_fall():
            pygame.event.post(EVENT_SOFT_DROP_LINE)
            self.fall()
    
    # move piece one left
    def left(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                # if part of the piece
                if self.current_piece[y][x] > 0:
                    # check if there is blocks below it or if it is at the bottom of the board
                    if self.board[self.current_y - y][self.current_x + x - 1] > 0 or self.current_x + x < 1:
                        return
        self.last_move_was_rotate = False
        self.current_x -= 1
                    
    # move piece one left
    def right(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                # if part of the piece
                if self.current_piece[y][x] > 0:
                    # check if there is blocks below it or if it is at the bottom of the board
                    try:
                        if self.board[self.current_y - y][self.current_x + x + 1] > 0:
                            return
                    except:
                        return
        self.last_move_was_rotate = False
        self.current_x += 1

    def intersecting(self, temp_x, temp_y):
        # check if in bounds
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                # if part of the piece
                if self.current_piece[y][x] > 0:
                    # check if there is blocks below it or if it is at the bottom of the board
                    if temp_y - y < 0 or temp_x + x < 0 or temp_x + x > 9:
                            return True
                    
        # check if intersects with piece
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                # if part of the piece
                if self.current_piece[y][x] > 0:
                    # check if there is blocks below it or if it is at the bottom of the board
                    if self.board[temp_y - y][temp_x + x] > 0:
                        return True
        
        return False
    
    # wall kicks
    # rotations: 0 = 90 | 1 = 180
    def valid_rotate(self, rotation):
        # check if normal rotation worked
        if self.intersecting(self.current_x, self.current_y):
            # if normal rotation didn't work then we have to try wallkicks
            # some pieces have special wall kicks
            # 90 degreee rotations
            if rotation == 0:
                # I piece
                if self.current_id == 1:
                    # (im only commenting this one cause all cases are the same just different kicks to loop through)
                    # loop through all possible wallkicks based on rotation amount, piece, and orignal and desired rotation positions
                    for mods in self.kick_table['90']['I'][(self.current_rotation, self.temp_rotation)]:
                        # set x and y respectivly
                        mod_x, mod_y = mods

                        # check if these wallkicks work
                        if not self.intersecting(self.current_x + mod_x, self.current_y + mod_y):
                            # if they do we will put them in place by changing the current x and y
                            self.current_x += mod_x
                            self.current_y += mod_y
                            self.current_rotation = self.temp_rotation
                            self.last_move_was_rotate = True
                            return True
                # all the other pieces
                else:
                    for mods in self.kick_table['90']['non-I'][(self.current_rotation, self.temp_rotation)]:
                        mod_x, mod_y = mods

                        if not self.intersecting(self.current_x + mod_x, self.current_y + mod_y):
                            self.current_x += mod_x
                            self.current_y += mod_y
                            self.current_rotation = self.temp_rotation
                            self.last_move_was_rotate = True
                            return True
            # 180 rotations
            else:
                for mods in self.kick_table['180'][(self.current_rotation, self.temp_rotation)]:
                    mod_x, mod_y = mods

                    if not self.intersecting(self.current_x + mod_x, self.current_y + mod_y):
                        self.current_x += mod_x
                        self.current_y += mod_y
                        self.current_rotation = self.temp_rotation
                        self.last_move_was_rotate = True
                        return True
        else:
            # if normal rotation worked then set that as the rotation
            self.current_rotation = self.temp_rotation
            self.last_move_was_rotate = True
            return True

    # rotate clockwise
    def rotate_cw(self):
        # add to rotation position
        self.temp_rotation = self.current_rotation + 1

        # make sure we dont add too much
        if self.temp_rotation == 4:
            self.temp_rotation = 0

        # squares are weird they will break but they dont rotate
        if self.current_id != 2:
            # rotate it doing weird grid stuff i figured out
            # pretty much i loop through the grid in different orders which causes it to flip
            temp_piece = []
            for i in range(len(self.current_piece[0])):
                temp_piece.append([])
                for j in range(len(self.current_piece) - 1, -1, -1):
                    temp_piece[i].append(self.current_piece[j][i])
            self.current_piece = temp_piece

            # make sure its a valid rotation (this will check and perform wallkicks too cause i made it very smart!!!)
            if not self.valid_rotate(0):
                # undo it by going backwards if it doesnt work
                self.rotate_ccw()

    # rotate counter clockwise
    def rotate_ccw(self):
        # takeaway from rotation position cause we going backwards
        self.temp_rotation = self.current_rotation - 1

        # dont takeaway too much
        if self.temp_rotation == -1:
            self.temp_rotation = 3

        # squares are weird they will break but they dont rotate
        if self.current_id != 2:
            # rotate it doing weird grid stuff i figured out
            # pretty much i loop through the grid in different orders which causes it to flip
            temp_piece = []
            for i in range(len(self.current_piece[0]) - 1, -1, -1):
                temp_row = []
                for j in range(len(self.current_piece)):
                    temp_row.append(self.current_piece[j][i])
                temp_piece.append(temp_row)
            self.current_piece = temp_piece

            # make sure its a valid rotation (this will check and perform wallkicks too cause i made it very smart!!!)
            if not self.valid_rotate(0):
                # undo it by going backwards if it doesnt work
                self.rotate_cw()

    # rotate 180
    def rotate_180(self):
        # add to our rotation position
        self.temp_rotation = self.current_rotation + 2

        # make sure rotation number doesnt go below 0 or above 3
        if self.temp_rotation == 4:
            self.temp_rotation = 0
        elif self.temp_rotation == 5:
            self.temp_rotation = 1

        # squares are weird they will break but they dont rotate
        if self.current_id != 2:
            # rotate it doing weird grid stuff i figured out
            # pretty much i loop through the grid in different orders which causes it to flip
            temp_piece = []
            for i in range(len(self.current_piece) - 1, -1, -1):
                temp_row = []
                for j in range(len(self.current_piece) - 1, -1, -1):
                    temp_row.append(self.current_piece[i][j])
                temp_piece.append(temp_row)
            # new rotated piece is set to the current piece orientation
            self.current_piece = temp_piece

        # make sure its a valid rotation (this will check and perform wallkicks too cause i made it very smart!!!)
        if not self.valid_rotate(1):
            # if it dont work just undo it by doing it again yk
            self.rotate_180()

    # holds current piece
    def hold_piece(self):
        # the new piece to spawn is whats being held rn
        new_piece = self.hold_id
        # the piece to be held
        self.hold_id = self.current_id
        # if hold piece exists spawn it
        if new_piece > 0:
            self.spawn_piece(new_piece)
        # if hold doesnt exist yet spawn next piece
        else:
            self.spawn_piece(self.next_pieces.pop(0))

