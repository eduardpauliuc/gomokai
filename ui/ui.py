from constants import Player
from game import Game
from strategies.random_strategy import RandomStrategy


class UI:
    def __init__(self, strategy):
        self._game = Game(strategy)

    @staticmethod
    def read_human_move():
        row = int(input('row>'))
        column = int(input('column>'))
        return row, column

    def start(self):
        human_turn = True

        while not self._game.is_game_finished:
            try:
                # Print the board state
                print(self._game.board)

                if human_turn:
                    coord = self.read_human_move()
                    # print(coord)
                    self._game.human_move(coord[0], coord[1], Player.BLACK)
                else:
                    self._game.computer_move(Player.WHITE)

                human_turn = not human_turn
            except ValueError as exception:
                print(exception)

        print(self._game.board)
        if self._game.board.board_winner == Player.WHITE:
            print('WHITE won the game!')
        elif self._game.board.board_winner == Player.BLACK:
            print('BLACK won the game!')
        else:
            print('DRAW!')
