# import pygame
# import sys
# import math
# import copy

# # --- CONSTANTS ---
# WIDTH = 600
# HEIGHT = 600
# LINE_WIDTH = 15
# WIN_LINE_WIDTH = 15
# BOARD_ROWS = 3
# BOARD_COLS = 3
# SQUARE_SIZE = WIDTH // BOARD_COLS
# CIRCLE_RADIUS = SQUARE_SIZE // 3
# CIRCLE_WIDTH = 15
# CROSS_WIDTH = 25
# SPACE = SQUARE_SIZE // 4

# # COLORS
# BG_COLOR = (28, 170, 156)
# LINE_COLOR = (23, 145, 135)
# CIRCLE_COLOR = (239, 231, 200)
# CROSS_COLOR = (66, 66, 66)

# class TicTacToe:
#     def __init__(self):
#         self.board = [' ' for _ in range(9)]
#         self.human = 'X'
#         self.ai = 'O'
#         self.current_player = self.human
#         self.game_over = False
#         self.winning_line = None # tuple of (start_index, end_index) for drawing

#     def available_moves(self):
#         return [i for i, spot in enumerate(self.board) if spot == ' ']

#     def empty_squares(self):
#         return ' ' in self.board

#     def num_empty_squares(self):
#         return self.board.count(' ')

#     def make_move(self, square, letter):
#         if self.board[square] == ' ':
#             self.board[square] = letter
#             return True
#         return False

#     def check_win(self, letter):
#         # Rows
#         for i in range(0, 9, 3):
#             if all([s == letter for s in self.board[i:i+3]]):
#                 self.winning_line = (i, i+2)
#                 return True
#         # Cols
#         for i in range(3):
#             if all([s == letter for s in [self.board[i+j*3] for j in range(3)]]): 
#                 self.winning_line = (i, i+6)
#                 return True
#         # Diagonals
#         if self.board[0] == letter and self.board[4] == letter and self.board[8] == letter:
#             self.winning_line = (0, 8)
#             return True
#         if self.board[2] == letter and self.board[4] == letter and self.board[6] == letter:
#             self.winning_line = (2, 6)
#             return True
#         return False

#     def check_draw(self):
#         return not self.empty_squares()

# # --- MINIMAX AGENT ---
# def minimax(game, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
#     # Check terminal states
#     if game.check_win(game.ai):
#         return 1 * (game.num_empty_squares() + 1)
#     elif game.check_win(game.human):
#         return -1 * (game.num_empty_squares() + 1)
#     elif not game.empty_squares():
#         return 0

#     if maximizing_player:
#         max_eval = -math.inf
#         for move in game.available_moves():
#             game.board[move] = game.ai
#             eval = minimax(game, depth + 1, False, alpha, beta)
#             game.board[move] = ' ' # Undo
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval
#     else:
#         min_eval = math.inf
#         for move in game.available_moves():
#             game.board[move] = game.human
#             eval = minimax(game, depth + 1, True, alpha, beta)
#             game.board[move] = ' ' # Undo
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval

# def get_best_move(game):
#     best_score = -math.inf
#     best_move = None
#     # Copy game state logic to avoid messing with current game instance visuals/state if needed
#     # But since minimax undoes moves, we can pass actual object IF we are careful.
#     # To be safe and clean, we rely on the undo in minimax.
    
#     # Simple check for immediate win/block helps speed but minimax handles it.
#     for move in game.available_moves():
#         game.board[move] = game.ai
#         score = minimax(game, 0, False)
#         game.board[move] = ' ' # Undo
#         if score > best_score:
#             best_score = score
#             best_move = move
#     return best_move

# # --- PYGAME DRAWING FUNCTIONS ---

# def draw_lines(screen):
#     # Horizontal
#     pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
#     pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
#     # Vertical
#     pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
#     pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# def draw_figures(screen, game):
#     for i in range(9):
#         val = game.board[i]
#         if val == ' ': continue
        
#         # Grid coords
#         row = i // 3
#         col = i % 3
#         x_pos = col * SQUARE_SIZE + SQUARE_SIZE // 2
#         y_pos = row * SQUARE_SIZE + SQUARE_SIZE // 2
        
#         if val == 'O':
#             pygame.draw.circle(screen, CIRCLE_COLOR, (x_pos, y_pos), CIRCLE_RADIUS, CIRCLE_WIDTH)
#         elif val == 'X':
#             # Descending line
#             pygame.draw.line(screen, CROSS_COLOR, 
#                              (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
#                              (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
#             # Ascending line
#             pygame.draw.line(screen, CROSS_COLOR, 
#                              (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
#                              (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

# def draw_winning_line(screen, start_idx, end_idx):
#     if start_idx is None or end_idx is None: return

#     row1, col1 = start_idx // 3, start_idx % 3
#     row2, col2 = end_idx // 3, end_idx % 3
    
#     x1 = col1 * SQUARE_SIZE + SQUARE_SIZE // 2
#     y1 = row1 * SQUARE_SIZE + SQUARE_SIZE // 2
#     x2 = col2 * SQUARE_SIZE + SQUARE_SIZE // 2
#     y2 = row2 * SQUARE_SIZE + SQUARE_SIZE // 2
    
#     pygame.draw.line(screen, CROSS_COLOR, (x1, y1), (x2, y2), WIN_LINE_WIDTH)

# # --- MAIN LOOP ---
# def main():
#     try:
#         pygame.init()
#     except Exception as e:
#         print(f"Error initializing Pygame: {e}")
#         print("Make sure to install it: pip install pygame")
#         return

#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption('TIC TAC TOE - AI EXAM Q3')
#     screen.fill(BG_COLOR)
#     draw_lines(screen)
    
#     game = TicTacToe()
    
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()

#             if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and game.current_player == game.human:
#                 mouseX = event.pos[0] # x
#                 mouseY = event.pos[1] # y

#                 clicked_row = int(mouseY // SQUARE_SIZE)
#                 clicked_col = int(mouseX // SQUARE_SIZE)
                
#                 index = clicked_row * 3 + clicked_col
                
#                 if game.available_moves() and game.make_move(index, game.human):
#                    if game.check_win(game.human):
#                         game.game_over = True
#                    elif game.check_draw():
#                         game.game_over = True
#                    else:
#                         game.current_player = game.ai
                
#         # AI Turn
#         if game.current_player == game.ai and not game.game_over:
#             # Simple delay or just run
#             pygame.display.update()
#             pygame.time.wait(500) # pause to look like thinking
            
#             best_move = get_best_move(game)
#             if best_move is not None:
#                 game.make_move(best_move, game.ai)
#                 if game.check_win(game.ai):
#                     game.game_over = True
#                 elif game.check_draw():
#                     game.game_over = True
#                 game.current_player = game.human

#         # Drawing
#         screen.fill(BG_COLOR)
#         draw_lines(screen)
#         draw_figures(screen, game)
        
#         if game.game_over and game.winning_line:
#             draw_winning_line(screen, game.winning_line[0], game.winning_line[1])
            
#         pygame.display.update()

# if __name__ == '__main__':
#     main()
