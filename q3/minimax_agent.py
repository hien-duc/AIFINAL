import math

def minimax(game, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
    """
    Minimax algorithm with Alpha-Beta Pruning.
    
    EXAM PSEUDOCODE MAPPING:
    function minimax(node, depth, maximizingPlayer)
        1. TERMINATION (BASE) CONDITIONS:
           if depth = 0 or node is a terminal node:
               return the heuristic value of node

        2. RECURSIVE STEP (MAXIMIZING):
           if maximizingPlayer:
               value := -infinity
               for each child of node:
                   value := max(value, minimax(child, depth - 1, FALSE))
                   alpha := max(alpha, value)
                   if beta <= alpha: break (* Beta Cutoff *)
               return value

        3. RECURSIVE STEP (MINIMIZING):
           else:
               value := +infinity
               for each child of node:
                   value := min(value, minimax(child, depth - 1, TRUE))
                   beta := min(beta, value)
                   if beta <= alpha: break (* Alpha Cutoff *)
               return value
    """
    
    # --- 1. TERMINATION (BASE) CONDITIONS ---
    # The recursion stops if someone has won or the board is full (tie).
    # We return a score: +10 for AI win, -10 for Human win, 0 for Tie.
    # We add/subtract 'num_empty_squares' to prefer winning SOONER.
    if game.check_win(game.ai):
        return 1 * (game.num_empty_squares() + 1)
    elif game.check_win(game.human):
        return -1 * (game.num_empty_squares() + 1)
    elif not game.empty_squares():
        return 0

    # --- 2. RECURSIVE STEP ---
    if maximizing_player:
        max_eval = -math.inf
        for move in game.available_moves():
            # Simulate the move
            game.board[move] = game.ai
            
            # Recursive call: Now it's the minimizing player's turn
            eval = minimax(game, depth + 1, False, alpha, beta)
            
            # Undo the move (Backtracking)
            game.board[move] = ' ' 
            
            # Maximize the result
            max_eval = max(max_eval, eval)
            
            # Alpha-Beta Pruning
            alpha = max(alpha, eval)
            if beta <= alpha:
                break # Beta Cutoff: Prune the rest of the branches
        return max_eval
    else:
        min_eval = math.inf
        for move in game.available_moves():
            # Simulate the move
            game.board[move] = game.human
            
            # Recursive call: Now it's the maximizing player's turn
            eval = minimax(game, depth + 1, True, alpha, beta)
            
            # Undo the move (Backtracking)
            game.board[move] = ' ' 
            
            # Minimize the result
            min_eval = min(min_eval, eval)
            
            # Alpha-Beta Pruning
            beta = min(beta, eval)
            if beta <= alpha:
                break # Alpha Cutoff: Prune the rest of the branches
        return min_eval

def get_best_move(game):
    """
    Determines the best move for the AI using Minimax.
    """
    best_score = -math.inf
    best_move = None
    
    for move in game.available_moves():
        game.board[move] = game.ai
        score = minimax(game, 0, False)
        game.board[move] = ' ' # Undo move
        if score > best_score:
            best_score = score
            best_move = move
    return best_move
