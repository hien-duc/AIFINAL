class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'
        self.current_player = self.human
        self.game_over = False
        self.winning_line = None # tuple of (start_index, end_index) for drawing

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

    # if using minimax_agent old comment this function
    def undo_move(self, square):
        self.board[square] = ' '

    def check_win(self, letter):
        # Rows
        for i in range(0, 9, 3):
            if all([s == letter for s in self.board[i:i+3]]):
                self.winning_line = (i, i+2)
                return True
        # Cols
        for i in range(3):
            if all([s == letter for s in [self.board[i+j*3] for j in range(3)]]): 
                self.winning_line = (i, i+6)
                return True
        # Diagonals
        if self.board[0] == letter and self.board[4] == letter and self.board[8] == letter:
            self.winning_line = (0, 8)
            return True
        if self.board[2] == letter and self.board[4] == letter and self.board[6] == letter:
            self.winning_line = (2, 6)
            return True
        return False

    def check_draw(self):
        return not self.empty_squares()
