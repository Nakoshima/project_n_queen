"""
N queens problem solver
"""
import copy
import random
import nqueen_solving_util as util


def print_board(size, board):
    """
    Prints the chessboard
    :param size: the size of the chessboard
    :param board: the chessboard
    """
    board_display = ''
    for row in range(size):
        for column in range(size):
            board_display += (' ' + str(board[row][column]))
        board_display += '\n'
    print(board_display, end='')


def can_t_attack(size, board):
    """
    Checks if no queen can attack another
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: True if no queen can attack, False if not
    """
    return util.can_t_attack(size, board)


def is_soluce(size, board):
    """
    Checks if a board is a solution to the n queens problem
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns:
        True if the board is a solution, False if not
        The number queens
    """
    # Counts the number of queens on the board
    nb_queen = sum([i.count(1) for i in board])
    return util.can_t_attack(size, board) and nb_queen == size, nb_queen


def solve_n_queen_small(size, board):
    """
    Solves small sized n queens problems by using
    a backtracking algorithm
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns:
        The board
        True if a solution is found, False if not
    """
    if size == 1:
        return [1], True

    if size < 4:
        return board, False

    # We start placing the queens from the bottom right
    row = size - 1

    return util.backtrack_n_queen(size, board, row), True


def solve_n_queen_all_soluce(size, board):
    """
    Finds all the solutions of a n queen problem
    by using a backtracking algorithm
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: Array of all of the possible solutions
    """
    if size == 1:
        return [[1]]

    if size < 4:
        return []

    return util.backtrack_all_soluce(size, board)


def solve_n_queen_big(size, board):
    """
    Solves big sized n queens problems by using
    based on the simulated annealing search
    Reasonable resolution time up to size = 200 (~1 min 30 s)
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns:
        The board
        True if a solution is found, False if not
    """
    queens = util.initial_state(size)

    current_heuristic = util.calculate_heuristic(queens)

    while current_heuristic != 0:
        # Chooses a random child board
        new_queens = copy.deepcopy(queens)

        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)

        # Temporarily swaps the queens if one of them is attacked
        if util.is_attacked(queens, i) or util.is_attacked(queens, j):
            new_queens[i], new_queens[j] = new_queens[j], new_queens[i]
            # If the new heuristic is lower than the current one
            # definitely swaps the queens
            if util.calculate_heuristic(new_queens) <= current_heuristic:
                queens = new_queens
        current_heuristic = util.calculate_heuristic(queens)
    board = util.fill_board(queens)
    return board, True
