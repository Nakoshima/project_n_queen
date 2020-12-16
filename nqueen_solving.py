def print_board(size, board):
    board_display = ''
    for line in range(size):
        for column in range(size):
            board_display += (' ' + str(board[line][column]))
        board_display += '\n'
    print(board_display, end = '')
        
def can_t_attack(size, board):
    for line in range(size):
        for column in range(size):
            if board[line][column] == 1:
                for i in range(size):
                    if board[line][i] == 1 and i != column:
                        return False
    
                    if board[i][column] == 1 and i != line:
                        return False

                    #diag bas droite
                    if line + i + 1 < size and column + i + 1 < size and board[line + i + 1][column + i + 1] == 1:
                        return False

                    #diag bas gauche
                    if line + i + 1 < size and column - i - 1 >= 0 and board[line + i + 1][column - i - 1] == 1:
                        return False
    return True
    
def is_soluce(size, board):
    nbQueen = 0
     
    for line in range(size):
        for column in range(size):
            if board[line][column] == 1:
                nbQueen += 1

    return can_t_attack(size, board) and nbQueen == size, nbQueen

def solve_n_queen_small(size, board):
    if(size < 4):
        return board, False
    
    line = size - 1
    while line > -1:
        for column in range(size - 1, -1, -1):
            #si la ligne contient un 1
            if 1 in board[line]:
                column = board[line].index(1) - 1
                board[line][column + 1] = 0

            board[line][column] = 1
            line = line - 1
            if not can_t_attack(size, board):                 
                board[line][column] = 0
                line = line + 1
            
            if column == 0 and 1 not in board[line]:
                line = line - 1

    # stack = [[size - 1, size - 1]]

    # while len(stack) > 0:
    #     pos = stack.pop()
    #     #vide le board
    #     board = [[0 for x in range(size)] for y in range(size)]
    #     #place la 1ère reine
    #     board[pos[0]][pos[1]] = 1

    #     #placement des reines restantes
    #     for line in range(size - 1, -1, -1):
    #         for column in range(size - 1, -1, -1):
    #             board[line][column] = 1
    #             if not can_t_attack(size, board):
    #                 board[line][column] = 0
    
    return board, True
             


def solve_n_queen_big(size, board):
    return [2]

def solve_n_queen_all_soluce(size, board):
    return [2]


board = [[0 for x in range(4)] for y in range(4)]
board, solved = solve_n_queen_small(4, board)
print_board(4, board)