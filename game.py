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

        # get screen
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
        # draws grid
        self.screen.blit(self.grid_sprite, (350, 100))

        # draw board pieces
        # every row below 22
        for row in range(22):
            # every cell
            for cell in range(10):
                # if not empty
                if self.board[row][cell] > 0:
                    # draw correct piece
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
            if self.next_pieces[piece] == 1:
                for row in range(3):
                    for cell in range(4):
                        if self.pieces[self.next_pieces[piece] - 1][row][cell] > 0:
                            self.screen.blit(self.piece_sprites[self.next_pieces[piece]], (cell*30+750, piece*100+row*30+105))
            elif self.next_pieces[piece] == 2:
                for row in range(2):
                    for cell in range(3):
                        if self.pieces[self.next_pieces[piece] - 1][row][cell] > 0:
                            self.screen.blit(self.piece_sprites[self.next_pieces[piece]], (cell*30+750, piece*100+row*30+105))
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
    def generate_bag(self):
        pieces = [1, 2, 3, 4, 5, 6, 7]
        random.shuffle(pieces)
        return pieces
    
    def can_spawn(self, piece):
        test_piece = self.pieces[piece - 1]

        for y in range(len(test_piece)):
            for x in range(len(test_piece[y])):
                if test_piece[y][x] > 0:
                    if self.board[21- y][3 + x] != 0:
                        return False
        return True
    
    def get_ghost(self):
        ghost_y = self.current_y

        while not self.intersecting(self.current_x, ghost_y):
            ghost_y -= 1

        ghost_y += 1

        return ghost_y

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
            # TODO: SWITCH TO GAMEOVER OR SOMETHING LIKE THAT
            pygame.event.post(pygame.event.Event(pygame.QUIT))

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

        # send proper event
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
    # rotation - 0 = 90 - 1 = 180
    def valid_rotate(self, rotation):
        if self.intersecting(self.current_x, self.current_y):
            if rotation == 0:
                if self.current_id == 1:
                    for mods in self.kick_table['90']['I'][(self.current_rotation, self.temp_rotation)]:
                        mod_x, mod_y = mods

                        if not self.intersecting(self.current_x + mod_x, self.current_y + mod_y):
                            self.current_x += mod_x
                            self.current_y += mod_y
                            self.current_rotation = self.temp_rotation
                            self.last_move_was_rotate = True
                            return True
                else:
                    for mods in self.kick_table['90']['non-I'][(self.current_rotation, self.temp_rotation)]:
                        mod_x, mod_y = mods

                        if not self.intersecting(self.current_x + mod_x, self.current_y + mod_y):
                            self.current_x += mod_x
                            self.current_y += mod_y
                            self.current_rotation = self.temp_rotation
                            self.last_move_was_rotate = True
                            return True
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
            self.current_rotation = self.temp_rotation
            self.last_move_was_rotate = True
            return True

    # rotate clockwise
    def rotate_cw(self):
        self.temp_rotation = self.current_rotation + 1

        if self.temp_rotation == 4:
            self.temp_rotation = 0

        # squares dont rotate and i did some weird stuff with squares
        if self.current_id != 2:
            temp_piece = []
            for i in range(len(self.current_piece[0])):
                temp_piece.append([])
                for j in range(len(self.current_piece) - 1, -1, -1):
                    temp_piece[i].append(self.current_piece[j][i])
            self.current_piece = temp_piece
        
            if not self.valid_rotate(0):
                self.rotate_ccw()

    # rotate counter clockwise
    def rotate_ccw(self):
        self.temp_rotation = self.current_rotation - 1

        if self.temp_rotation == -1:
            self.temp_rotation = 3

        # squares dont rotate and i did some weird stuff with squares
        if self.current_id != 2:
            temp_piece = []
            for i in range(len(self.current_piece[0]) - 1, -1, -1):
                temp_row = []
                for j in range(len(self.current_piece)):
                    temp_row.append(self.current_piece[j][i])
                temp_piece.append(temp_row)
            self.current_piece = temp_piece

            if not self.valid_rotate(0):
                self.rotate_cw()

    # rotate 180
    def rotate_180(self):
        self.temp_rotation = self.current_rotation + 2

        if self.temp_rotation == 4:
            self.temp_rotation = 0
        elif self.temp_rotation == 5:
            self.temp_rotation = 1

        if self.current_id != 2:
            temp_piece = []
            for i in range(len(self.current_piece) - 1, -1, -1):
                temp_row = []
                for j in range(len(self.current_piece) - 1, -1, -1):
                    temp_row.append(self.current_piece[i][j])
                temp_piece.append(temp_row)
            self.current_piece = temp_piece

        if not self.valid_rotate(1):
            self.rotate_180()

    def hold_piece(self):
        new_piece = self.hold_id
        self.hold_id = self.current_id
        if new_piece > 0:
            self.spawn_piece(new_piece)
        else:
            self.spawn_piece(self.next_pieces.pop(0))

