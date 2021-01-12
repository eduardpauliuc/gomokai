from texttable import Texttable

from constants import Player, row_change, col_change


class Board:
    """
    Class that manages the Gomoku board
    """

    def __init__(self, board_size, previous_data=None):
        """
        Initializes the Gomoku Board
        :param board_size: integer
        :param previous_data: if the board is a duplicate of another board, this is a matrix
                              with previous board data. This is copied to prevent shallow copy problems
        """
        self._board_size = board_size
        self._board_winner = Player.NONE
        self._last_move_line = None
        self._last_move_column = None
        self._number_of_empty_cells = board_size * board_size

        if previous_data is not None:
            self._data = [[previous_data[row][col] for col in range(board_size)] for row in range(board_size)]
        else:
            self._data = [[Player.NONE for j in range(self._board_size)] for i in range(self._board_size)]

    @property
    def board_size(self):
        return self._board_size

    @property
    def board_winner(self):
        return self._board_winner

    @property
    def last_move(self):
        return self._last_move_line, self._last_move_column

    @property
    def is_draw(self):
        return self._number_of_empty_cells == 0

    @property
    def data(self):
        return self._data

    def get_cell_value(self, row, column):
        """
        Gets the value at row and column
        :param row: integer in range [0, board size-1]
        :param column: integer in range [0, board size-1]
        :return: Player.NONE or Player.WHITE or Player.BLACK
        """
        return self._data[row][column]

    def is_cell_empty(self, row, column):
        """
        Checks if cell at row and column is empty
        :param row: integer in range [0, board size-1]
        :param column: integer in range [0, board size-1]
        :return: True if value is NONE and False if value is not NONE
        """
        return self.get_cell_value(row, column) == Player.NONE

    def get_filled_cells(self):
        """
        Returns a list of tuples (row,column) that already have a piece placed
        :return: list of two integer tuples
        """
        return [(row, column) for column in range(self.board_size) for row in range(self.board_size) if
                not self.is_cell_empty(row, column)]

    def set(self, row, column, player_colour):
        """
        Places a piece at (row, column) and then updates the board status.
        Checks if the piece made someone a winner
        :param row: integer in range [0, board size]
        :param column: integer in range [0, board size]
        :param player_colour: Player.WHITE or Player.BLACK
        """
        self._data[row][column] = player_colour
        self._number_of_empty_cells -= 1
        self._last_move_line, self._last_move_column = row, column
        self._check_for_winner()

    def set_without_checking(self, row, column, player_colour):
        """
        Places a piece at (row, column) but does not check if it made someone a winner
        :param row: integer in range [0, board size-1]
        :param column: integer in range [0, board size-1]
        :param player_colour: Player.WHITE or Player.BLACK
        :return:
        """
        self._data[row][column] = player_colour

    def are_coordinates_valid(self, row, column):
        """
        Checks if row and column are in the valid range
        :param row: integer
        :param column: integer
        :return: True if coordinates are valid and False otherwise
        """
        return 0 <= row < self.board_size and 0 <= column < self._board_size

    def _check_for_winner(self):
        """
        Checks if there is a winner in the current board placement.
        If there is a winner, it is marked in the "self._board_winner" attribute of the board.
        """
        for direction in range(4):
            row, column = self._last_move_line, self._last_move_column
            line = self.get_line_of_characters(row, column, direction, must_be_the_same=True)

            if 'W' * 5 in line:
                self._board_winner = Player.WHITE
            elif 'B' * 5 in line:
                self._board_winner = Player.BLACK

    def __str__(self):
        """
        Returns string representation of the table in Texttable format
        :return: string
        """
        t = Texttable()

        t.header([' '] + [str(i) for i in range(self.board_size)])
        for row in range(self.board_size):
            row_data = []

            for value in self._data[row]:
                row_data.append(self.cell_to_character(value))

            t.add_row([str(row)] + row_data)

        return t.draw()

    def get_line_of_characters(self, row, col, direction, must_be_the_same=False):
        """
        From a given cell, gets row/column/diagonal in the direction specified
        Beginning from the cell, it expands at most 7 cells in both directions
        If must_be_the_same is True, it only expands if the next cells are the same with the given cell
        :param row: integer in range [0, board size-1]
        :param col: integer in range [0, board size-1]
        :param direction: integer in range [0, 7], 0 being north and going clockwise
        :param must_be_the_same: optional boolean character
        :return: string with characters ' ', 'B' and 'W'
        """
        cell_value = self.get_cell_value(row, col)
        line = self.cell_to_character(cell_value)

        new_row, new_col = row, col
        length = 0

        while self.are_coordinates_valid(new_row + row_change[direction], new_col + col_change[direction]) \
                and length < 7:

            if must_be_the_same and self.get_cell_value(new_row + row_change[direction],
                                                        new_col + col_change[direction]) != cell_value:
                break

            length += 1
            new_row += row_change[direction]
            new_col += col_change[direction]
            line = line + self.cell_to_character(self.get_cell_value(new_row, new_col))

        new_row, new_col = row, col
        length = 0

        while self.are_coordinates_valid(new_row - row_change[direction], new_col - col_change[direction]) \
                and length < 7:

            if must_be_the_same and self.get_cell_value(new_row - row_change[direction],
                                                        new_col - col_change[direction]) != cell_value:
                break

            length += 1
            new_row -= row_change[direction]
            new_col -= col_change[direction]
            line = self.cell_to_character(self.get_cell_value(new_row, new_col)) + line

        return line

    @staticmethod
    def cell_to_character(value):
        """
        Converts Player value to one character
        :param value: Player.BLACK, Player.NONE or Player.WHITE
        :return: 'B', ' ' or 'W'
        """
        if value == Player.BLACK:
            return 'B'
        elif value == Player.WHITE:
            return 'W'
        else:
            return ' '
