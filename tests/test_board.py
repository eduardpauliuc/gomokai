import unittest

from board import Board
from constants import Player


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_board(self):
        board = Board(11)

        self.assertEqual(board.board_size, 11)
        self.assertEqual(board.board_winner, Player.NONE)

        board.set(1, 2, Player.WHITE)
        self.assertEqual(board.get_line_of_characters(1, 2, 2, True), 'W')
        self.assertEqual(board.get_cell_value(1, 2), Player.WHITE)
        self.assertEqual(board.last_move, (1, 2))
        board.set(1, 3, Player.BLACK)
        board.set(1, 4, Player.BLACK)
        board.set(1, 5, Player.BLACK)
        board.set(1, 6, Player.BLACK)
        board.set(1, 7, Player.BLACK)
        self.assertEqual(board.board_winner, Player.BLACK)
        self.assertEqual(board.are_coordinates_valid(11, 20), False)
