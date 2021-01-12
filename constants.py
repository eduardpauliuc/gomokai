from enum import Enum

BOARD_SIZE = 11

WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#222222"

row_change = [-1, -1, 0, 1, 1, 1, 0, -1]
col_change = [0, 1, 1, 1, 0, -1, -1, -1]


class Player(Enum):
    NONE = 0
    BLACK = 1
    WHITE = 2
