import pygame
import sys
import constants
from game_logic import TicTacToe
from minimax_agent import get_best_move

# --- PYGAME DRAWING TRIGGERS ---

def draw_lines(screen):
    # Horizontal
    pygame.draw.line(screen, constants.LINE_COLOR, (0, constants.SQUARE_SIZE), (constants.WIDTH, constants.SQUARE_SIZE), constants.LINE_WIDTH)
    pygame.draw.line(screen, constants.LINE_COLOR, (0, 2 * constants.SQUARE_SIZE), (constants.WIDTH, 2 * constants.SQUARE_SIZE), constants.LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, constants.LINE_COLOR, (constants.SQUARE_SIZE, 0), (constants.SQUARE_SIZE, constants.HEIGHT), constants.LINE_WIDTH)
    pygame.draw.line(screen, constants.LINE_COLOR, (2 * constants.SQUARE_SIZE, 0), (2 * constants.SQUARE_SIZE, constants.HEIGHT), constants.LINE_WIDTH)

def draw_figures(screen, game):
    for i in range(9):
        val = game.board[i]
        if val == ' ': continue
        
        # Grid coords
        row = i // 3
        col = i % 3
        x_pos = col * constants.SQUARE_SIZE + constants.SQUARE_SIZE // 2
        y_pos = row * constants.SQUARE_SIZE + constants.SQUARE_SIZE // 2
        
        if val == 'O':
            pygame.draw.circle(screen, constants.CIRCLE_COLOR, (x_pos, y_pos), constants.CIRCLE_RADIUS, constants.CIRCLE_WIDTH)
        elif val == 'X':
            # Descending line
            pygame.draw.line(screen, constants.CROSS_COLOR, 
                             (col * constants.SQUARE_SIZE + constants.SPACE, row * constants.SQUARE_SIZE + constants.SPACE), 
                             (col * constants.SQUARE_SIZE + constants.SQUARE_SIZE - constants.SPACE, row * constants.SQUARE_SIZE + constants.SQUARE_SIZE - constants.SPACE), constants.CROSS_WIDTH)
            # Ascending line
            pygame.draw.line(screen, constants.CROSS_COLOR, 
                             (col * constants.SQUARE_SIZE + constants.SPACE, row * constants.SQUARE_SIZE + constants.SQUARE_SIZE - constants.SPACE), 
                             (col * constants.SQUARE_SIZE + constants.SQUARE_SIZE - constants.SPACE, row * constants.SQUARE_SIZE + constants.SPACE), constants.CROSS_WIDTH)

def draw_winning_line(screen, start_idx, end_idx):
    if start_idx is None or end_idx is None: return

    row1, col1 = start_idx // 3, start_idx % 3
    row2, col2 = end_idx // 3, end_idx % 3
    
    x1 = col1 * constants.SQUARE_SIZE + constants.SQUARE_SIZE // 2
    y1 = row1 * constants.SQUARE_SIZE + constants.SQUARE_SIZE // 2
    x2 = col2 * constants.SQUARE_SIZE + constants.SQUARE_SIZE // 2
    y2 = row2 * constants.SQUARE_SIZE + constants.SQUARE_SIZE // 2
    
    pygame.draw.line(screen, constants.CROSS_COLOR, (x1, y1), (x2, y2), constants.WIN_LINE_WIDTH)

# --- MAIN LOOP ---
def main():
    try:
        pygame.init()
    except Exception as e:
        print(f"Error initializing Pygame: {e}")
        print("Make sure to install it: pip install pygame")
        return

    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption('TIC TAC TOE - AI EXAM Q3')
    screen.fill(constants.BG_COLOR)
    draw_lines(screen)
    
    game = TicTacToe()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and game.current_player == game.human:
                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y

                clicked_row = int(mouseY // constants.SQUARE_SIZE)
                clicked_col = int(mouseX // constants.SQUARE_SIZE)
                
                index = clicked_row * 3 + clicked_col
                
                if game.available_moves() and game.make_move(index, game.human):
                   if game.check_win(game.human):
                        game.game_over = True
                   elif game.check_draw():
                        game.game_over = True
                   else:
                        game.current_player = game.ai
                
        # AI Turn
        if game.current_player == game.ai and not game.game_over:
            pygame.display.update()
            pygame.time.wait(500) # pause
            
            best_move = get_best_move(game)
            if best_move is not None:
                game.make_move(best_move, game.ai)
                if game.check_win(game.ai):
                    game.game_over = True
                elif game.check_draw():
                    game.game_over = True
                game.current_player = game.human

        # Drawing
        screen.fill(constants.BG_COLOR)
        draw_lines(screen)
        draw_figures(screen, game)
        
        if game.game_over and game.winning_line:
            draw_winning_line(screen, game.winning_line[0], game.winning_line[1])
            
        pygame.display.update()

if __name__ == '__main__':
    main()
