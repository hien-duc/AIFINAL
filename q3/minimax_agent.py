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
    
    RELATION TO THEORY PSEUDOCODE:
    This function combines 'MAX-VALUE' and 'MIN-VALUE' into one function 
    using the 'maximizing_player' boolean flag.
    
    - if maximizing_player is True: Acts as MAX-VALUE(game, state)
    - if maximizing_player is False: Acts as MIN-VALUE(game, state)
    """
    
    # --- 1. TERMINATION (BASE) CONDITIONS ---
    # Equivalent to: if game.IS-TERMINAL(state) then return game.UTILITY(state, player)
    if game.check_win(game.ai):
        return 1 * (game.num_empty_squares() + 1)
    elif game.check_win(game.human):
        return -1 * (game.num_empty_squares() + 1)
    elif not game.empty_squares():
        return 0

    # --- 2. RECURSIVE STEP (MAX-VALUE) ---
    if maximizing_player:
        max_eval = -math.inf
        for move in game.available_moves():
            # Simulate (game.RESULT)
            game.board[move] = game.ai
            
            # Recursive call (MIN-VALUE)
            eval = minimax(game, depth + 1, False, alpha, beta)
            
            # Backtrack
            game.board[move] = ' ' 
            
            # Logic: v = max(v, v2)
            max_eval = max(max_eval, eval)
            
            # Alpha-Beta
            alpha = max(alpha, eval)
            if beta <= alpha:
                break 
        return max_eval
    
    # --- 3. RECURSIVE STEP (MIN-VALUE) ---
    else:
        min_eval = math.inf
        for move in game.available_moves():
            # Simulate (game.RESULT)
            game.board[move] = game.human
            
            # Recursive call (MAX-VALUE)
            eval = minimax(game, depth + 1, True, alpha, beta)
            
            # Backtrack
            game.board[move] = ' ' 
            
            # Logic: v = min(v, v2)
            min_eval = min(min_eval, eval)
            
            # Alpha-Beta
            beta = min(beta, eval)
            if beta <= alpha:
                break 
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
