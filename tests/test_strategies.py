import unittest

from board import Board
from constants import Player
from strategies.minmax_strategy import MinmaxStrategy
from strategies.random_strategy import RandomStrategy


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board(11)

    def test_random(self):
        strategy = RandomStrategy()

        self.board.set(1, 1, Player.WHITE)
        last_move = strategy.make_move(self.board, Player.BLACK)
        self.assertEqual(self.board.last_move, last_move)

    def test_minmax(self):
        strategy = MinmaxStrategy()

        self.board.set(1, 1, Player.WHITE)
        self.board.set(1, 2, Player.WHITE)
        self.board.set(1, 3, Player.WHITE)
        self.board.set(1, 5, Player.WHITE)

        last_move = strategy.make_move(self.board, Player.BLACK)
        self.assertEqual((1, 4), last_move)
        self.board.set_without_checking(1, 4, Player.NONE)
        last_move = strategy.make_move(self.board, Player.WHITE)
        self.assertEqual((1, 4), last_move)
