import math

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)] # 0-8
        self.human = 'X'
        self.ai = 'O'

    def print_board(self):
        b = self.board
        print(f"{b[0]} | {b[1]} | {b[2]}")
        print("--+---+--")
        print(f"{b[3]} | {b[4]} | {b[5]}")
        print("--+---+--")
        print(f"{b[6]} | {b[7]} | {b[8]}")
        print("\n")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            return True
        return False

    def winner(self, square, letter):
        # check row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True
        # check col
        col_ind = square % 3
        col = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in col]):
            return True
        # check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

def minimax(game, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
    """
    Minimax with Alpha-Beta Pruning.
    
    Pseudocode:
    function minimax(node, depth, maximizingPlayer)
        if depth = 0 or node is a terminal node
            return the heuristic value of node
        
        if maximizingPlayer
            value := -infinity
            for each child of node
                value := max(value, minimax(child, depth - 1, FALSE))
                alpha := max(alpha, value)
                if beta <= alpha
                    break (* Beta cutoff *)
            return value
        else
            value := +infinity
            for each child of node
                value := min(value, minimax(child, depth - 1, TRUE))
                beta := min(beta, value)
                if beta <= alpha
                    break (* Alpha cutoff *)
            return value
    """
    
    # Base Conditions / Termination
    current_state_winner = None
    # We need to check if the PREVIOUS move won. 
    # Since we don't pass the last move, we scan the board for a winner.
    # Helper to detect winner based on state:
    if check_win(game.board, game.ai):
        return 1 * (game.num_empty_squares() + 1) # Prefer faster wins
    elif check_win(game.board, game.human):
        return -1 * (game.num_empty_squares() + 1)
    elif not game.empty_squares():
        return 0 # Tie

    if maximizing_player:
        max_eval = -math.inf
        for move in game.available_moves():
            game.board[move] = game.ai
            eval = minimax(game, depth + 1, False, alpha, beta)
            game.board[move] = ' ' # Undo move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in game.available_moves():
            game.board[move] = game.human
            eval = minimax(game, depth + 1, True, alpha, beta)
            game.board[move] = ' ' # Undo move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Helper for global win check
def check_win(board, letter):
    # Rows
    for i in range(0, 9, 3):
        if all([s == letter for s in board[i:i+3]]): return True
    # Cols
    for i in range(3):
        if all([s == letter for s in [board[i+j*3] for j in range(3)]]): return True
    # Diagonals
    if board[0] == letter and board[4] == letter and board[8] == letter: return True
    if board[2] == letter and board[4] == letter and board[6] == letter: return True
    return False

def get_best_move(game):
    best_score = -math.inf
    best_move = None
    for move in game.available_moves():
        game.board[move] = game.ai
        score = minimax(game, 0, False)
        game.board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def play_game():
    game = TicTacToe()
    game.print_board()
    
    while game.empty_squares():
        # Human Move
        try:
            square = int(input("Input move (0-8): "))
            if square not in game.available_moves():
                print("Invalid move.")
                continue
        except ValueError:
            print("Invalid input.")
            continue
            
        game.make_move(square, game.human)
        game.print_board()
        
        if check_win(game.board, game.human):
            print("Human wins!")
            return
            
        if not game.empty_squares():
            print("Tie!")
            return

        # AI Move
        print("AI Thinking...")
        square = get_best_move(game)
        game.make_move(square, game.ai)
        game.print_board()
        
        if check_win(game.board, game.ai):
            print("AI wins!")
            return
            
        if not game.empty_squares():
            print("Tie!")
            return

if __name__ == '__main__':
    play_game()
