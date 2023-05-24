import pygame

SINGLE_LINE = pygame.USEREVENT + 1
DOUBLE_LINE = pygame.USEREVENT + 2
TRIPLE_LINE = pygame.USEREVENT + 3
TETRIS_LINE = pygame.USEREVENT + 4
SPIN = pygame.USEREVENT + 10
MINI_SPIN = pygame.USEREVENT + 11
MINI_SINGLE_SPIN = pygame.USEREVENT + 12
SINGLE_SPIN = pygame.USEREVENT + 13
DOUBLE_SPIN = pygame.USEREVENT + 14
TRIPLE_SPIN = pygame.USEREVENT + 15
SINGLE_CLEAR = pygame.USEREVENT + 20
DOUBLE_CLEAR = pygame.USEREVENT + 21
TRIPLE_CLEAR = pygame.USEREVENT + 22
TETRIS_CLEAR = pygame.USEREVENT + 23
HARD_DROP_LINE = pygame.USEREVENT + 30
SOFT_DROP_LINE = pygame.USEREVENT + 31
LINE = pygame.USEREVENT + 100

EVENT_SINGLE_LINE = pygame.event.Event(SINGLE_LINE)
EVENT_DOUBLE_LINE = pygame.event.Event(DOUBLE_LINE)
EVENT_TRIPLE_LINE = pygame.event.Event(TRIPLE_LINE)
EVENT_TETRIS_LINE = pygame.event.Event(TETRIS_LINE)
EVENT_SPIN = pygame.event.Event(SPIN)
EVENT_MINI_SPIN = pygame.event.Event(MINI_SPIN)
EVENT_MINI_SINGLE_SPIN = pygame.event.Event(MINI_SINGLE_SPIN)
EVENT_SINGLE_SPIN = pygame.event.Event(SINGLE_SPIN)
EVENT_DOUBLE_SPIN = pygame.event.Event(DOUBLE_SPIN)
EVENT_TRIPLE_SPIN = pygame.event.Event(TRIPLE_SPIN)
EVENT_SINGLE_CLEAR = pygame.event.Event(SINGLE_CLEAR)
EVENT_DOUBLE_CLEAR = pygame.event.Event(DOUBLE_CLEAR)
EVENT_TRIPLE_CLEAR = pygame.event.Event(TRIPLE_CLEAR)
EVENT_TETRIS_CLEAR = pygame.event.Event(TETRIS_CLEAR)
EVENT_HARD_DROP_LINE = pygame.event.Event(HARD_DROP_LINE)
EVENT_SOFT_DROP_LINE = pygame.event.Event(SOFT_DROP_LINE)
EVENT_LINE = pygame.event.Event(LINE)