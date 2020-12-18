def print_board(size, board):
    board_display = ''
    for line in range(size):
        for column in range(size):
            board_display += (' ' + str(board[line][column]))
        board_display += '\n'
    print(board_display, end = '')
        
def can_t_attack(size, board):
    for line in range(size):
        # compter directement le nb de reine sur une ligne en une fois au lieu de boucler
        nbQueen = board[line].count(1)
        if nbQueen > 1:
            return False
        
        if nbQueen == 1:
            # obtenir directement la colonne de la reine lieu de boucler puisqu'on sait qu'il n'y a qu'une reine sur la ligne ici
            column = board[line].index(1)
            
            # on n'a besoin de check qu'en dessous de la reine actuelle
            for i in range(line + 1, size):
                # bas
                if board[i][column] == 1:
                    return False

                #diag bas droite
                if column + i - line < size and board[i][column + i - line] == 1:
                    return False

                #diag bas gauche
                if column - (i - line) >= 0 and board[i][column - (i - line)] == 1:
                    return False    
    return True
    
def is_soluce(size, board):
    # compte le nombre de reine dans tout le board
    nbQueen = sum([i.count(1) for i in board])

    return can_t_attack(size, board) and nbQueen == size, nbQueen

def solve_n_queen_small(size, board):
    if(size < 4):
        return board, False
    
    line = size - 1
    while not is_soluce(size, board)[0]:
        for column in range(size - 1, -1, -1):
            #si la ligne contient un 1 et que on la parcourt, cela signifie que le 1 est mal placé alors on le retire et on en place 1 à la position suivante
            while 1 in board[line]:
                column = board[line].index(1) - 1
                board[line][column + 1] = 0
                if column == -1:
                    line = line + 1
                    column = size - 1

            board[line][column] = 1
            line = line - 1
            
            #### debug
            print_board(8, board)
            print('')
            time.sleep(0.2)
            #### debug
            
            if not can_t_attack(size, board):
                line = line + 1
                #la ligne que j'ai changé par accident... et hop ça fonctionne comme par magie...
                #board[line][column] = 0
            else:
                break
            
            # if column == 0 and 1 not in board[line]:
            #     line = line + 1

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
