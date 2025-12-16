from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax, X, O, EMPTY

def test_game():
    print("Testing implementation...")
    
    # 1. Test Initial State
    board = initial_state()
    assert player(board) == X, "Initial player should be X"
    assert not terminal(board), "Initial board should not be terminal"
    print("PASS: Initial State properties")
    
    # 2. Test Player Logic (After 1 move)
    board = result(board, (0, 0)) # X moves
    assert player(board) == O, "After X moves, it should be O's turn"
    print("PASS: Player Turn Logic")
    
    # 3. Test Winner (Row)
    # X X X
    # O O .
    # . . .
    board = [[X, X, X], [O, O, EMPTY], [EMPTY, EMPTY, EMPTY]]
    assert winner(board) == X, "Row of X should win"
    assert terminal(board), "Board with winner should be terminal"
    assert utility(board) == 1, "X win utility should be 1"
    print("PASS: Win Detection")
    
    # 4. Test Minimax (Prevent Loss)
    # X X .
    # O O .
    # . . .
    # If it is O's turn, O MUST move to (1, 2) to win immediately logic?
    # Actually let's test a block.
    # X X . 
    # . O .
    # . . .
    # If it is O's turn (impossible here but let's assume valid state), O should block or try to win?
    # Let's try "Find winning move":
    # X X .
    # O O .
    # . . . 
    # Current player X's turn if we balance it? No let's construct a valid near-win state.
    
    # Valid State: X turn, can win immediately
    # X X .
    # O O .
    # . . .
    # X needs to pick (0, 2)
    board = [[X, X, EMPTY],
             [O, O, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    # Check whose turn it is
    # X: 2, O: 2 -> It is X's turn
    assert player(board) == X
    print("Testing Minimax X Winning move...")
    move = minimax(board)
    print(f"Minimax suggested: {move}")
    assert move == (0, 2), "X should pick (0, 2) to win"
    print("PASS: Minimax Found Win")

    print("\nALL CONSTRAINED TESTS PASSED.")

if __name__ == "__main__":
    test_game()
