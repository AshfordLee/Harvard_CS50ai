"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # raise NotImplementedError
    num_of_x=0
    num_of_o=0
    for row in board:
        for cell in row:
            if cell==X:
                num_of_x+=1
            if cell==O:
                num_of_o+=1

    if num_of_x==0 or num_of_x==num_of_o:
        return X
    
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # raise NotImplementedError
    actions=set()
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                actions.add((i,j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # raise NotImplementedError
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    new_board=copy.deepcopy(board)
    current_player=player(board)
    
    row,col=action

    new_board[row][col]=current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # raise NotImplementedError
    
    for row in board:
        if row.count(X)==3:
            return X
        
        if row.count(O)==3:
            return O
        
    for i in range(3):
        if board[0][i]==board[1][i]==board[2][i]==X:
            return X
        
        if board[0][i]==board[1][i]==board[2][i]==O:
            return O
        
    if board[0][0]==board[1][1]==board[2][2]==X:
        return X
    
    if board[0][0]==board[1][1]==board[2][2]==O:
        return O
    
    if board[0][2]==board[1][1]==board[2][0]==X:
        return X
    
    if board[0][2]==board[1][1]==board[2][0]==O:
        return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # raise NotImplementedError

    if winner(board) is not None:
        return True
    
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                return False

    return True 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # raise NotImplementedError
    if winner(board)==X:
        return 1
    
    if winner(board)==O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # raise NotImplementedError
    if terminal(board):
        return None
    
    current_player=player(board)

    possible_actions=actions(board)

    if current_player==X:
        best_score=float('-inf')
        best_action=None

        for action in possible_actions:
            new_board=result(board,action)
            score=min_value(new_board)

            if score>best_score:
                best_score=score
                best_action=action


        return best_action
    
    else:
        best_score=float('inf')
        best_action=None

        for action in possible_actions:
            new_board=result(board,action)
            score=max_value(new_board)

            if score<best_score:
                best_score=score
                best_action=action

        return best_action

def max_value(board):

    if terminal(board):
        return utility(board)
    
    value=float('-inf')

    for action in actions(board):

        new_board=result(board,action)

        value=max(value,min_value(new_board))

    return value

def min_value(board):
    
    if terminal(board):
        return utility(board)
    
    value=float('inf')

    for action in actions(board):

        new_board=result(board,action)

        value=min(value,max_value(new_board))

    return value