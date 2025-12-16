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
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    
    # X goes first, so if counts are equal, it's X's turn.
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action")
    
    # Create deep copy
    new_board = copy.deepcopy(board)
    current_player = player(board)
    
    i, j = action
    new_board[i][j] = current_player
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check Rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    # Check Columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]

    # Check Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    # Check for empty cells (if any empty, game not over)
    for row in board:
        if EMPTY in row:
            return False
            
    # Tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    current_player = player(board)
    
    if current_player == X:
        # X is Maximizing player
        v = -math.inf
        # "choose the action with highest max value"
        # We need to find the action associated with the max value, not just the value.
        best_action = None
        for action in actions(board):
            # v = max(v, min_value(result(board, action))) -- this is just value
            # We need to track the action
            val = min_value(result(board, action), -math.inf, math.inf)
            if val > v:
                v = val
                best_action = action
        return best_action

    else:
        # O is Minimizing player
        v = math.inf
        best_action = None
        for action in actions(board):
            val = max_value(result(board, action), -math.inf, math.inf)
            if val < v:
                v = val
                best_action = action
        return best_action


def max_value(board, alpha, beta):
    """
    Returns the max value for X (Maximizer), using Alpha-Beta Pruning.
    """
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        # Recursive call to min_value
        v = max(v, min_value(result(board, action), alpha, beta))
        
        # Alpha update
        alpha = max(alpha, v)
        
        # Beta Cutoff
        if v >= beta:
            return v
            
    return v


def min_value(board, alpha, beta):
    """
    Returns the min value for O (Minimizer), using Alpha-Beta Pruning.
    """
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        
        # Beta update
        beta = min(beta, v)
        
        # Alpha Cutoff
        if v <= alpha:
            return v
            
    return v
