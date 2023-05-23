import pygame
import random

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


        # generate first two bags
        next_pieces = self.generate_bag() + self.generate_bag()

        current_piece = self.pieces[next_pieces.pop(0) - 1]
        current_x = 3
        current_y = 21

    # draws the game
    def draw(self):
        # draws grid
        self.screen.blit(self.grid_sprite, (350, 100))

        # draw current piece
        

        # every row below 22
        for row in range(22):
            # every cell
            for cell in range(10):
                # if not empty
                if self.board[row][cell] > 0:
                    # draw correct piece
                    self.screen.blit(self.piece_sprites[self.board[row][cell]], (cell*30+355, (19-row)*30+105))

    # generates next piece bag
    def generate_bag(self):
        pieces = [1, 2, 3, 4, 5, 6, 7]
        random.shuffle(pieces)
        return pieces
    
    def spawn_piece(self, piece):
