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
    for line in range(size):
        for column in range(size):
            board_display += (' ' + str(board[line][column]))
        board_display += '\n'
    print(board_display, end = '')

def is_soluce(size, board):
    """
    Checks if a board is a solution to the n queens problem
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: True if the board is a solution, False if not and the number of the queens
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
    :returns: the board and True if a solution is found, False if not
    """
    if size == 1:
        return [1], True

    if size < 4:
        return board, False

    # We start placing the queens from the bottom right
    line = size - 1

    # Calls the backtracking algorithm
    return util.backtrack_n_queen(size, board, line), True

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
    Reasonable resolution time up to size = 150 (~1 min 30 s)
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: the board and True if a solution is found, False if not
    """
    current_queens = util.initial_state(size)

    while util.calculate_heuristic(current_queens) != 0:
        # Chooses a random child board
        new_queens = copy.deepcopy(current_queens)
        index1 = random.randint(0, size - 1)
        index2 = random.randint(0, size - 1)

        # Temporarily swaps the queens if one of them is attacked
        if util.is_attacked(current_queens, index1) or util.is_attacked(current_queens, index2):
            new_queens[index1], new_queens[index2] = new_queens[index2], new_queens[index1]
            # Definitely swaps the queens if the new heuristic is lower than the current one
            if util.calculate_heuristic(new_queens) <= util.calculate_heuristic(current_queens):
                current_queens = new_queens
    board = util.fill_board(current_queens)
    return board, True
