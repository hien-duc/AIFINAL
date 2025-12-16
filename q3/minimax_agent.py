import math

# =============================================================================
# NEW IMPLEMENTATION (Strictly Matching Pseudocode Image)
# =============================================================================

def get_best_move(game):
    """
    Entry point for the AI agent.
    """
    # Uses the new ALPHA-BETA-SEARCH function
    best_move = alpha_beta_search(game, game.board)
    return best_move

def alpha_beta_search(game, state):
    """
    function ALPHA-BETA-SEARCH(game, state) returns an action
    """
    # player <- game.To-MOVE(state)
    # The game logic handles turns internally, but for the root call we are the 'player' (AI - 'O')
    
    # value, move <- MAX-VALUE(game, state, -infinity, +infinity)
    utility, move = max_value(game, state, -math.inf, math.inf)
    
    # return move
    return move

def max_value(game, state, alpha, beta):
    """
    function MAX-VALUE(game, state, alpha, beta) returns a (utility, move) pair
    """
    # if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    if game.check_win(game.ai): return 10, None      # AI ('O') Wins
    if game.check_win(game.human): return -10, None  # Human ('X') Wins
    if not game.empty_squares(): return 0, None      # Draw
    
    # v <- -infinity
    v = -math.inf
    best_move = None
    
    # for each a in game.ACTIONS(state) do
    actions = game.available_moves()
    
    for action in actions:
        game.make_move(action, game.ai) # Apply Action 'a'
        
        # v2, a2 <- MIN-VALUE(game, game.RESULT(state, a), alpha, beta)
        # We pass 'state' but since we modified 'game' in place, it represents the new state.
        v2, _ = min_value(game, state, alpha, beta)
        
        game.undo_move(action) # Backtrack (Restore state)
        
        # if v2 > v then
        if v2 > v:
            # v, move <- v2, a
            v = v2
            best_move = action
            
            # alpha <- MAX(alpha, v)
            alpha = max(alpha, v)
        
        # if v >= beta then return v, move
        if v >= beta:
            return v, best_move
            
    # return v, move
    return v, best_move

def min_value(game, state, alpha, beta):
    """
    function MIN-VALUE(game, state, alpha, beta) returns a (utility, move) pair
    """
    # if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    if game.check_win(game.ai): return 10, None
    if game.check_win(game.human): return -10, None
    if not game.empty_squares(): return 0, None
    
    # v <- +infinity
    v = math.inf
    best_move = None
    
    # for each a in game.ACTIONS(state) do
    actions = game.available_moves()
    
    for action in actions:
        game.make_move(action, game.human) # Apply Action 'a' (Human turn)
        
        # v2, a2 <- MAX-VALUE(game, game.RESULT(state, a), alpha, beta)
        v2, _ = max_value(game, state, alpha, beta)
        
        game.undo_move(action)
        
        # if v2 < v then
        if v2 < v:
            # v, move <- v2, a
            v = v2
            best_move = action
            
            # beta <- MIN(beta, v)
            beta = min(beta, v)
            
        # if v <= alpha then return v, move
        if v <= alpha:
            return v, best_move
            
    # return v, move
    return v, best_move


# =============================================================================
# OLD IMPLEMENTATION (Single Recursive Function) - COMMENTED OUT
# =============================================================================
#
# def get_best_move_old(game):
#     best_score = -math.inf
#     best_move = None
#     alpha = -math.inf
#     beta = math.inf
#     
#     # We maximize for 'O' (AI)
#     for move in game.available_moves():
#         game.make_move(move, 'O')
#         score = minimax_old(game, 0, False, alpha, beta)
#         game.undo_move(move)
#         
#         if score > best_score:
#             best_score = score
#             best_move = move
#         
#         alpha = max(alpha, score)
#         if beta <= alpha:
#             break
#             
#     return best_move
#
# def minimax_old(game, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
#     """
#     Minimax algorithm with Alpha-Beta Pruning.
#     EXAM PSEUDOCODE MAPPING:
#     function minimax(node, depth, maximizingPlayer)
#         1. TERMINATION (BASE) CONDITIONS:
#            if depth = 0 or node is a terminal node:
#                return the heuristic value of node
#
#         2. RECURSIVE STEP (MAXIMIZING):
#            if maximizingPlayer:
#                value := -infinity
#                for each child of node:
#                    value := max(value, minimax(child, depth - 1, FALSE))
#                    alpha := max(alpha, value)
#                    if beta <= alpha: break (* Beta Cutoff *)
#                return value
#
#         3. RECURSIVE STEP (MINIMIZING):
#            else:
#                value := +infinity
#                for each child of node:
#                    value := min(value, minimax(child, depth - 1, TRUE))
#                    beta := min(beta, value)
#                    if beta <= alpha: break (* Alpha Cutoff *)
#                return value
#     
#     RELATION TO THEORY PSEUDOCODE:
#     This function combines 'MAX-VALUE' and 'MIN-VALUE' into one function 
#     using the 'maximizing_player' boolean flag.
#     """
#     
#     # ------------------------------------------------------------------------------
#     # 1. TERMINATION CONDITIONS (Base)
#     # ------------------------------------------------------------------------------
#     if game.check_win('O'):  return 1   # AI won
#     if game.check_win('X'):  return -1  # Human won
#     if not game.empty_squares(): return 0   # Draw
#     
#     # ------------------------------------------------------------------------------
#     # 2. RECURSIVE STEP - MAXIMIZING (AI's Turn)
#     # Matches: function MAX-VALUE(state, alpha, beta)
#     # ------------------------------------------------------------------------------
#     if maximizing_player:
#         max_eval = -math.inf
#         for move in game.available_moves():
#             game.make_move(move, 'O')
#             
#             # Recursive Call
#             eval = minimax_old(game, depth + 1, False, alpha, beta)
#             
#             game.undo_move(move)
#             max_eval = max(max_eval, eval)
#             
#             # Alpha-Beta Update
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break # Pruning
#         return max_eval
#     
#     # ------------------------------------------------------------------------------
#     # 3. RECURSIVE STEP - MINIMIZING (Opponent's Turn)
#     # Matches: function MIN-VALUE(state, alpha, beta)
#     # ------------------------------------------------------------------------------
#     else:
#         min_eval = math.inf
#         for move in game.available_moves():
#             game.make_move(move, 'X')
#             
#             # Recursive Call
#             eval = minimax_old(game, depth + 1, True, alpha, beta)
#             
#             game.undo_move(move)
#             min_eval = min(min_eval, eval)
#             
#             # Alpha-Beta Update
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break # Pruning
#         return min_eval
