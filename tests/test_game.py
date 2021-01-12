import unittest

from constants import Player
from game import Game
from strategies.random_strategy import RandomStrategy


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_game(self):
        strategy = RandomStrategy()
        game = Game(strategy)
        game.human_move(1, 1, Player.BLACK)

        self.assertEqual(game.is_game_finished, False)

        self.assertRaises(ValueError, game.human_move, 1, 11, Player.WHITE)
        self.assertRaises(ValueError, game.human_move, 11, 1, Player.WHITE)
        self.assertRaises(ValueError, game.human_move, 1, 1, Player.WHITE)

        move = game.computer_move(Player.WHITE)
        self.assertNotEqual(move, (1, 1))

        game.restart()
        self.assertEqual(game.board.get_cell_value(1, 1), Player.NONE)
