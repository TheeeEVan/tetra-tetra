import pygame
import random

class Game():
    def __init__(self):
        self.grid_sprite = pygame.image.load("assets/grid.png")

        # create a 10x40 grid
        # without multiplayer, chances of using more than 20 rows is very low but we'll use proper playing area with the idea of expanding later
        # (color, active?)
        # COLORS:
        # 1 - cyan
        # 2 - yellow
        # 3 - purple
        # 4 - green
        # 5 - red
        # 6 - blue
        # 7 - orange
        self.grid = [
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]], # bottom of grid
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]],
            [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]  # top of grid (doesnt make sense here but it will when we draw)
        ]

        self.nexts = self.generate_bag() + self.generate_bag()
        self.bag_number = 0 # used so every 7 pieces we create new bag

        self.piece_left = 0
        self.piece_right = 0
        self.piece_bottom = 0

        self.spawn_piece()

        self.next_grid = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]

        self.update_nexts()

    # generates bag for next 7 pieces
    def generate_bag(self):
        bag = [1,2,3,4,5,6,7]
        random.shuffle(bag)
        return bag
    
    def update_nexts(self):
        for i in range(5):
            if self.nexts[i] == 1:
                self.next_grid[3*i] =   [1,1,1,1]
                self.next_grid[3*i+1] = [0,0,0,0]
            elif self.nexts[i] == 2:
                self.next_grid[3*i] =   [0,2,2,0]
                self.next_grid[3*i+1] = [0,2,2,0]
            elif self.nexts[i] == 3:
                self.next_grid[3*i] =   [0,3,0,0]
                self.next_grid[3*i+1] = [3,3,3,0]
            elif self.nexts[i] == 4:
                self.next_grid[3*i] =   [0,4,4,0]
                self.next_grid[3*i+1] = [4,4,0,0]
            elif self.nexts[i] == 5:
                self.next_grid[3*i] =   [5,5,0,0]
                self.next_grid[3*i+1] = [0,5,5,0]
            elif self.nexts[i] == 6:
                self.next_grid[3*i] =   [6,0,0,0]
                self.next_grid[3*i+1] = [6,6,6,0]
            elif self.nexts[i] == 7:
                self.next_grid[3*i] =   [0,0,7,0]
                self.next_grid[3*i+1] = [7,7,7,0]

    def spawn_piece(self):
        piece = self.nexts.pop(0)
        self.bag_number += 1

        if self.bag_number > 7:
            self.nexts += self.generate_bag()
            self.update_nexts()

        if piece == 1:
            self.grid[20][3] = [1, 1, 0]
            self.grid[20][4] = [1, 1, 1]
            self.grid[20][5] = [1, 1, 0]
            self.grid[20][6] = [1, 1, 0]
            self.piece_left = 3
            self.piece_right = 6
            self.piece_bottom = 20
        elif piece == 2:
            self.grid[20][4] = [2, 1, 0]
            self.grid[20][5] = [2, 1, 0]
            self.grid[21][4] = [2, 1, 0]
            self.grid[21][5] = [2, 1, 0]
            self.piece_left = 4
            self.piece_right = 5
            self.piece_bottom = 20
        elif piece == 3:
            self.grid[20][3] = [3, 1, 0]
            self.grid[20][4] = [3, 1, 1]
            self.grid[20][5] = [3, 1, 0]
            self.grid[21][4] = [3, 1, 0]
            self.piece_left = 3
            self.piece_right = 5
            self.piece_bottom = 20
        elif piece == 4:
            self.grid[20][3] = [4, 1, 0]
            self.grid[20][4] = [4, 1, 1]
            self.grid[21][4] = [4, 1, 0]
            self.grid[21][5] = [4, 1, 0]
            self.piece_left = 3
            self.piece_right = 5
            self.piece_bottom = 20
        elif piece == 5:
            self.grid[20][4] = [5, 1, 1]
            self.grid[20][5] = [5, 1, 0]
            self.grid[21][3] = [5, 1, 0]
            self.grid[21][4] = [5, 1, 0]
            self.piece_left = 3
            self.piece_right = 5
            self.piece_bottom = 20
        elif piece == 6:
            self.grid[20][3] = [6, 1, 0]
            self.grid[20][4] = [6, 1, 1]
            self.grid[20][5] = [6, 1, 0]
            self.grid[21][3] = [6, 1, 0]
            self.piece_left = 3
            self.piece_right = 5
            self.piece_bottom = 20
        elif piece == 7:
            self.grid[20][3] = [7, 1, 0]
            self.grid[20][4] = [7, 1, 1]
            self.grid[20][5] = [7, 1, 0]
            self.grid[21][5] = [7, 1, 0]
            self.piece_left = 3
            self.piece_right = 5
            self.piece_bottom = 20

    def can_fall(self):
        # first check if bottomed out
        if self.piece_bottom == 0:
            return False
        for cell in range(10):
            if self.grid[self.piece_bottom][cell][1] == 1:
                if self.grid[self.piece_bottom - 1][cell][0] != 0:
                    return False
                
        return True

    def fall(self):
        if self.can_fall():
            self.piece_bottom -= 1
            for row in range(22):
                for cell in range(10):
                    if self.grid[row][cell][1] == 1:
                        self.grid[row - 1][cell] = self.grid[row][cell]
                        self.grid[row][cell] = [0, 0]
        else:
            self.lock()

    def lock(self):
        for row in range(22):
            for cell in range(10):
                self.grid[row][cell][1] = 0

        self.spawn_piece()
    
    def left(self):
        if self.piece_left > 0:
            self.piece_right -= 1
            self.piece_left -= 1
            for row in range(22):
                    for cell in range(10):
                        if self.grid[row][cell][1] == 1:
                            self.grid[row][cell - 1] = self.grid[row][cell]
                            self.grid[row][cell] = [0, 0]

    def right(self):
        if self.piece_right < 9:
            self.piece_right += 1
            self.piece_left += 1
            for row in range(22):
                    for cell in range(9, -1, -1):
                        if self.grid[row][cell][1] == 1:
                            self.grid[row][cell + 1] = self.grid[row][cell]
                            self.grid[row][cell] = [0, 0]
    
    def drop(self):
        while self.can_fall():
            self.fall()
        self.lock()

