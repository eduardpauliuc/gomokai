from abc import ABC, abstractmethod


class Strategy(ABC):
    """
    Abstract class that should be implemented by strategies
    """
    @abstractmethod
    def make_move(self, board, player_colour) -> object:
        """
        This should apply a move to the board and also return the move made, that is a tuple of two integers
        :param board: Board object
        :param player_colour: player at move
        :return: tuple of two integers
        """
        pass
