"""
Module docstring
"""
import time
import copy
import random


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

def is_soluce(size, board):
    """
    Checks if a board is a solution to the n queens problem

    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: True if the board is a solution, False if not
    """
    # Counts the number of queens on the board
    nb_queen = sum([i.count(1) for i in board])
    return can_t_attack(size, board) and nb_queen == size, nb_queen

def solve_n_queen_small(size, board):
    """
    Backtracking algorithm solving the n queens problem
    Reasonable resolution time up to size = 26 (~1 min 30 s)

    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: the board and True if a solution is found, False if not
    """
    if size < 4:
        return board, False

    # We start placing the queens from the bottom right
    line = size - 1

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
                    line = line + 1
                    column = size - 1

            # Places a queen on the current line
            board[line][column] = 1

            if can_t_attack(size, board):
                # Moves up to the next line
                line = line - 1
                # Breaking the for loop so that the column scan can start over
                break
    return board, True

def solve_n_queen_all_soluce(size, board):
    """
    Finds all the solutions of a n queen problem
    By using the backtracking algorithm

    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: Array of all of the possible solutions
    """
    boards = []

    if size < 4:
        return boards

    # dernière ligne du board
    line = size - 1

    # condition d'arret
    while True:
        while line > -1:
            for column in range(size - 1, -1, -1):
                while 1 in board[line]:
                    column = board[line].index(1) - 1
                    board[line][column + 1] = 0
                    # si on est à la première colonne
                    # il n'y plus de placement de reine possible sur la ligne courante
                    # donc on change le placement de la reine du dessous
                    if column == -1:
                        # si on est redescendu jusqu'à la dernière ligne
                        # il n'y a plus d'autre solution
                        if line == size - 1:
                            return boards
                        line = line + 1
                        column = size - 1

                board[line][column] = 1
                line = line - 1

                # si une reine peut attaquer
                if not can_t_attack(size, board):
                    line = line + 1
                else:
                    break
        boards.append(copy.deepcopy(board))
        line = line + 1

def solve_n_queen_big(size, board):
    """
    Algorithm solving the n queens problem
    Based on the simulated annealing search
    Reasonable resolution time up to size = 150 (~1 min 30 s)

    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: the board and True if a solution is found, False if not
    """
    current_queens = initial_state(size)
    board = fill_board(current_queens)
    # ### debug
    # print_board(size, board)
    # print(calculate_heuristic(size, board))
    # print('')
    # time.sleep(0.2)
    # ### debug
    while calculate_heuristic(size, board) != 0:
        # choix aléatoire d'un état (plateau) enfant
        new_queens = copy.deepcopy(current_queens)
        index1 = random.randint(0, size - 1)
        index2 = random.randint(0, size - 1)
        new_queens[index1], new_queens[index2] = new_queens[index2], new_queens[index1]

        new_board = fill_board(new_queens)
        # ### debug
        # print_board(size, new_board)
        # print("nouvelle heuristique : " + str(calculate_heuristic(size, new_board)))
        # print('')
        # time.sleep(0.2)
        # ### debug

        if calculate_heuristic(size, board) >= calculate_heuristic(size, new_board):
            board = new_board
            current_queens = new_queens
            # ## debug
            # print_board(size, board)
            # print(calculate_heuristic(size, board))
            # print('')
            # # time.sleep(0.2)
            # ## debug

    return board, True

def initial_state(size):
    """
    Gets a random initial state of the board
    with one queen per column and per line

    :param size: the size of the chessboard
    :returns: Array with the queens' position
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

    :param queens: an array containing the position of each queens
    :returns: the fill board
    """
    board = [[0 for x in enumerate(queens)] for y in enumerate(queens)]
    for i in enumerate(queens):
        board[i][queens[i]] = 1
    return board

def calculate_heuristic(size, board):
    """
    Calculates the heuristic of a chessboard
    (the number of possible direct and indirect attacks)

    :param size: the size of the chessboard
    :param board: the chessboard
    :returns: the number of possible attacks
    """
    heuristic = 0
    for line in range(size):
        # obtenir directement la colonne de la reine lieu de boucler
        # puisqu'on sait qu'il n'y a qu'une reine sur la ligne ici
        column = board[line].index(1)

        # on a besoin de check qu'en dessous de la reine actuelle
        # en digonale car on génère un board avec des reines
        # sur des lignes et colonnes différentes
        for i in range(line + 1, size):
            #diag bas droite
            if column + i - line < size and board[i][column + i - line] == 1:
                heuristic += 1

            #diag bas gauche
            if column - (i - line) >= 0 and board[i][column - (i - line)] == 1:
                heuristic += 1
    return heuristic


BOARD_SIZE = 26

t1 = time.time()
test_board = [[0 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
# board_soluce, found = solve_n_queen_big(BOARD_SIZE, test_board)
board_soluce, found = solve_n_queen_small(BOARD_SIZE, test_board)
t2 = time.time()
print_board(BOARD_SIZE, board_soluce)
print(f"\nTest of size {BOARD_SIZE} took {t2-t1} seconds to be solved")
