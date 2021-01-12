from board import Board
from constants import col_change, row_change, Player, BOARD_SIZE
from strategies.strategy import Strategy

INF = int(7e12)
DEPTH = 4


# noinspection DuplicatedCode
class MinmaxStrategy(Strategy):
    """
    Strategy that uses Minmax algorithm with alpha-beta pruning to compute next move
    """
    # Scores used to evaluate a given board, + being a piece of the player at move and - the other player
    HEURISTIC_SCORES = {
        "-----": -1000000000000,
        "+++++": 1000000000000,
        " ---- ": -50000000000,
        " ++++ ": 10000000000,
        "-++++ ": 100000000,
        " ++++-": 100000000,
        " ----+": -500000000,
        "+---- ": -500000000,
        " +++ ": 1000,
        " +++-": 150,
        " ---+": -50,
        " --- ": -5000,
        " ++ ": 10,
        " -- ": -50
    }

    def make_move(self, board, player_colour) -> tuple:
        """
        Computes and applies a move to the board
        :param board: Board object
        :param player_colour: Player.WHITE or Player.BLACK
        :return: tuple of two integers, coordinates of computed move
        """
        temporary_board = Board(BOARD_SIZE, board.data[:])
        initial_possibilities = self.get_possible_cells(board, [], board.get_filled_cells())

        best_score, best_move = self.minmax(temporary_board, DEPTH, True, -INF, INF,
                                            initial_possibilities, player_colour,
                                            [])
        print('Computed move: ' + str(best_move) + ' score: ' + str(best_score))
        board.set(*best_move, player_colour)
        return best_move

    def minmax(self, board, depth, is_maximizing, alpha, beta, important_cells, player_colour, moves_so_far):
        """
        Recursive function that implements the minmax algorithm.
        The end case is at depth 0, when it stops and evaluates the current board.
        For each depth, chooses appropriate "board score", considering if the player is maximizing or not
        Optimizes the recursion tree by using alpha-beta pruning
        :param board: Board object
        :param depth: Current depth of the recursion
        :param is_maximizing: Boolean. True if current player is Maximizer and False if current player is Minimizer
        :param alpha: integer value
        :param beta: integer value
        :param important_cells: list of (row,column) integer tuples, represent cells around which pieces might be placed
        :param player_colour:  Player.WHITE or Player.BLACk
        :param moves_so_far: list of (row,column) integer tuples, represent moves made so far in the recursion tree
        :return: tuple with (best score of the move, (row,column) of the best move)
        """
        if depth == 0:
            return self.evaluate_board(board, player_colour, moves_so_far), None

        next_player = Player.BLACK if player_colour == Player.WHITE else Player.WHITE
        options = self.get_possible_cells(board, important_cells, moves_so_far)

        if is_maximizing:
            best_score, best_move = -INF, None

            for move in options:
                row, column = move
                if board.get_cell_value(row, column) is not Player.NONE:
                    continue

                temporary_board = Board(BOARD_SIZE, board.data[:])

                temporary_board.set(row, column, player_colour)
                moves_so_far.append((row, column))
                if temporary_board.board_winner != Player.NONE:
                    value = INF - 1
                else:
                    value, _ = self.minmax(temporary_board, depth - 1, False, alpha, beta, important_cells,
                                           next_player, moves_so_far)

                moves_so_far.pop(-1)

                if value > best_score:
                    best_score, best_move = value, move

                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        else:
            best_score, best_move = INF, None

            for move in options:
                row, column = move
                if board.get_cell_value(row, column) is not Player.NONE:
                    continue

                temporary_board = Board(BOARD_SIZE, board.data[:])
                temporary_board.set(row, column, player_colour)
                moves_so_far.append((row, column))
                if temporary_board.board_winner != Player.NONE:
                    value = -INF + 1
                else:
                    value, _ = self.minmax(temporary_board, depth - 1, True, alpha, beta, important_cells,
                                           next_player, moves_so_far)

                moves_so_far.pop(-1)

                if value < best_score:
                    best_score, best_move = value, move

                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score, best_move

    def get_possible_cells(self, board, important_cells, moves_so_far):
        """
        Generates the cells that should be checked further, in a heuristic manner.
        Checking every cell on the board is too computationally expensive, so we have to
        heuristically sort the possible next moves by a score, given by the get_cell_importance function.
        :param moves_so_far: list of (row,column), representing cells already placed in the recursion tree
        :param board: Board object
        :param important_cells: list of (row,column), places on the board that have pieces
        :return: list of moves, as tuples of two integers, sorted by score, descending
        """
        cells = set(important_cells)

        for row, column in moves_so_far:
            for direction in range(8):
                new_row = row + row_change[direction]
                new_column = column + col_change[direction]

                if board.are_coordinates_valid(new_row, new_column) and \
                        board.get_cell_value(new_row, new_column) == Player.NONE:
                    cells.add((new_row, new_column))

        cells = list(cells) + moves_so_far

        return sorted(cells, key=lambda cell: self.get_cell_importance(board, *cell), reverse=True)[:10]

    def evaluate_board(self, board, player, moves_so_far):
        """
        Heuristic function to evaluate the entire board.
        :param board: Board object
        :param player: Player.WHITE or Player.BLACK, maximizer player
        :param moves_so_far: list of (row,column), representing cells already placed in the recursion tree
        :return: The score of the whole board, after evaluation
        """
        score = 0
        maximizer = board.cell_to_character(player)
        minimizer = 'B' if maximizer == 'W' else 'W'

        for row, column in moves_so_far:
            for direction in range(4):
                line = board.get_line_of_characters(row, column, direction)
                line = line.replace(maximizer, '+').replace(minimizer, '-')

                values = {}
                substrings = [line[i:i + length] for length in [4, 5, 6] for i in range(len(line)) if
                              i + length < len(line)]
                for substring in substrings:
                    values[substring] = values[substring] + 1 if substring in values else 1

                for item in self.HEURISTIC_SCORES.keys():
                    score += self.HEURISTIC_SCORES[item] * values[item] if item in values else 0

        return score

    @staticmethod
    def get_cell_importance(board, row, column):
        """
        Heuristic that computes the importance of a given piece on the board,
        depending on the length of the same colour piece line it forms
        :param board: Board object
        :param row: integer in range [0, board size - 1]
        :param column: integer in range [0, board size - 1]
        :return: Integer value denoting the importance
        """
        if board.get_cell_value(row, column) != Player.NONE:
            return 0
        value = 0

        board.set_without_checking(row, column, Player.WHITE)
        for direction in range(4):
            value += len(board.get_line_of_characters(row, column, direction, must_be_the_same=True)) ** 3

        board.set_without_checking(row, column, Player.BLACK)
        for direction in range(4):
            value += len(board.get_line_of_characters(row, column, direction, must_be_the_same=True)) ** 3

        board.set_without_checking(row, column, Player.NONE)

        return value
