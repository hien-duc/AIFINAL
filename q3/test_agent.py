from game_logic import TicTacToe
from minimax_agent import get_best_move

game = TicTacToe()
# Simulate a state where AI can win or block
# X | X |  
# O | O |  
#   |   |  
game.make_move(0, 'X')
game.make_move(3, 'O')
game.make_move(1, 'X')
game.make_move(4, 'O')

print("Board State:")
print(game.board)
print("AI 'O' to move. Should pick index 5 to win immediately.")

move = get_best_move(game)
print(f"AI Selected Move: {move}")

if move == 5:
    print("TEST PASSED: AI found the winning move.")
else:
    print("TEST FAILED: AI did not pick 5.")
