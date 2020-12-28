"""
N queens problem solver utility functions
"""
import copy
import random

def can_t_attack(size, board):
    """
    Checks if no queen can attack another
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: True if no queen can attack, False if not
    """
    for line in range(size):
        nb_queen = board[line].count(1)

        # If there is more than one queen on the line
        # then there is a possible attack
        if nb_queen > 1:
            return False

        if nb_queen == 1:
            # There is only one queen on the current line so we can get its position on the column
            column = board[line].index(1)

            # Only need to check the squares under the current queen
            for i in range(line + 1, size):
                # Bottom
                if board[i][column] == 1:
                    return False

                # Bottom right diagonal
                if column + i - line < size and board[i][column + i - line] == 1:
                    return False

                # Bottom left diagonal
                if column - (i - line) >= 0 and board[i][column - (i - line)] == 1:
                    return False
    return True

def backtrack_n_queen(size, board, line):
    """
    Backtracking algorithm solving the n queens problem (only one solution)
    Reasonable resolution time up to size = 26 (~1 min 30 s)
    :param size: the size of the chessboard
    :param board: the chessboard
    :param line: the row where we want to place the queen on
    :returns: the board and True if a solution is found, False if not
    """
    # The condition means the algorithm has gone through all the lines
    # and all the queens are safely placed
    while line > -1:
        # From right to left
        for column in range(size - 1, -1, -1):
            # If the current line contains a queen
            # that means it is not the first iteration and that a queen can attack
            # So we remove the queen and place it to the next square on the left
            while 1 in board[line]:
                column = board[line].index(1) - 1
                board[line][column + 1] = 0
                if column == -1:
                    # If we went back down the board
                    # then there is no possible solution left
                    if line == size - 1:
                        return None
                    line = line + 1
                    column = size - 1

            # Places a queen on the current line
            board[line][column] = 1

            if can_t_attack(size, board):
                # Moves up to the next line
                line = line - 1
                # Breaking the for loop so that the column scan can start over
                break
    return board

def backtrack_all_soluce(size, board):
    """
    Backtracking algorithm solving the n queens problem (all the solutions)
    Reasonable resolution time up to size = 13 (~40 s)
    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: the board and True if a solution is found, False if not
    """
    boards = []
    line = size - 1

    while True:
        new_solution = backtrack_n_queen(size, board, line)
        if new_solution is None:
            return boards
        boards.append(copy.deepcopy(new_solution))
        line = 0

def initial_state(size):
    """
    Gets a random initial state of the board
    with one queen per column and per line
    :param size: the size of the chessboard
    :returns: an 1D array with the queens' position
    """
    # Array containing the position of the queens
    # The indexes correspond to the board's lines
    # The values correpond to the board's columns
    queens = list(i for i in range(size))
    random.shuffle(queens)
    return queens

def fill_board(queens):
    """
    Fills the chessboard with queens
    :param queens: an 1D array containing the position of each queens
    :returns: the fill board
    """
    board = [[0 for x in enumerate(queens)] for y in enumerate(queens)]
    for row, col in enumerate(queens):
        board[row][col] = 1
    return board

def calculate_heuristic(queens):
    """
    Calculates the heuristic of a chessboard
    (the number of possible direct and indirect attacks)
    where the queens are placed on different rows and columns
    :param queens: an 1D array containing the position of each queens
    :returns: the number of possible attacks
    """
    heuristic = 0
    # For each queen except the last one,
    # checks if an attack to the next queens is possible
    for row in range(len(queens) - 1):
        for next_row in range(row + 1, len(queens)):
            # An attack is possible only if two queens are on the same diagonal,
            # that is to say, if the difference between their rows is equal to
            # the difference between their columns
            if abs(row - next_row) == abs(queens[row] - queens[next_row]):
                heuristic += 1
    return heuristic

def is_attacked(queens, index):
    """
    Checks if a queen is attacked by another one
    :param queens: an 1D array containing the position of each queens
    :param index: the index (also row) of the queen in the array queens
    """
    for row, col in enumerate(queens):
        if index != row:
            if abs(index - row) == abs(queens[index] - col):
                return True
    return False
