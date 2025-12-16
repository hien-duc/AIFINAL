# AI Exam Study Guide & Algorithm Explanations

This guide explains the core concepts for the three exam questions to help you understand **HOW** and **WHY** they work.

---

## 1. Depth-First Search (DFS) & The "Node Position" Error

### Concept
DFS explores a graph by going as deep as possible along each branch before backtracking. It uses a **Stack (LIFO - Last In, First Out)** data structure.
*   **LIFO**: The last element added is the first one processed.

### The "Node Position" Issue (Q1)
This question tests your understanding of **order of operations** in a stack.

*   **Scenario**: You are at Node `S`. It has neighbors `[A, B]` (in that order).
*   **The Mistake**: If you simply push `A` then `B` onto the stack:
    1. Stack becomes: `[A, B]` (Bottom -> Top).
    2. `pop()` removes `B` first.
    3. You visit `B` before `A`.
    *   *Result*: You traverse the graph Right-to-Left, which might be "wrong" if the problem expects alphabetical/Left-to-Right order.
*   **The Correction**: To visit `A` first, you must push `A` **LAST** (so it is on top).
    1. Reverse the neighbors: `[B, A]`.
    2. Push `B`. Stack: `[B]`.
    3. Push `A`. Stack: `[B, A]`.
    4. `pop()` removes `A`.
    *   *Result*: You visit `A` first.

---

## 2. Adversarial Search vs. Standard Search (Q2)

### Why DFS fails in Games (Tic-Tac-Toe / Chess)
*   **DFS Assumption**: "I can choose all my future moves."
*   **Reality in Games**: You choose, then the **Opponent** chooses.
*   **The Problem**: DFS looks for *a* path to a win. It might find a path: "I move X, then I move Y, then I move Z -> Win!" DFS thinks this is a solution. But in reality, after you move X, the opponent might move Block-Y, completely preventing your path. DFS essentially "hopes" the opponent won't interfere.

### Minimax Solution
*   **Minimax Assumption**: "My opponent is smart and will always play the move that is **worst** for me."
*   **MAX (You)**: Tries to pick the move with the highest score.
*   **MIN (Opponent)**: Tries to pick the move with the lowest score (worst for you).
*   Minimax finds the strategy that guarantees the best possible outcome *even if the opponent plays perfectly*.

---

## 3. Minimax with Alpha-Beta Pruning (Q3)

### The Algorithm
Minimax is a recursive algorithm that dives to the end of the game (or a depth limit), evaluates who won, and sends that score back up.

*   **Base Case (Termination)**: Check if the game is over (Win/Loss/Tie). If so, return +1 (Win), -1 (Loss), or 0 (Tie).
*   **Recursive Step**:
    *   If it's **My Turn (MAX)**: Look at all moves, ask "What is the result of this?", and pick the **maximum** value.
    *   If it's **Opponent's Turn (MIN)**: Look at all moves, ask "What is the result?", and pick the **minimum** value (because they want me to lose).

### Alpha-Beta Pruning (The Optimization)
Minimax checks *every* possible game state, which is slow. Pruning allows us to **stop checking** branches we know are useless.

*   **Alpha ($\alpha$)**: The best (highest) score that the **Maximizer** can guarantee so far.
*   **Beta ($\beta$)**: The best (lowest) score that the **Minimizer** can guarantee so far.

#### How it works (The Intuition)
Imagine you are MAX. You have two moves, A and B.
1.  You check Move A. It leads to a score of **5**.
    *   So, you know you can get *at least* 5. ($\alpha = 5$).
2.  You check Move B. The opponent (MIN) replies to B.
    *   The opponent finds a reply to B that gives you a score of **3**.
3.  **The Cutoff**: You stop analyzing Move B right there.
    *   *Why?* The opponent can force you into a score of 3 if you pick B. But you already know Move A gives you 5. You will **NEVER** pick B because 3 < 5. It doesn't matter if Move B *could* have led to a 100 later down a different branch; the opponent has a "kill move" that limits it to 3, so you prune it.


---

## 4. Code & Line-by-Line Analysis

### 4.1 DFS Correction (Q1)

```python
def dfs_corrected(problem, limit):
    frontier = [problem.initial]  # 1. Stack with Start Node
    
    while frontier:               # 2. Loop while stack has nodes
        node = frontier.pop()     # 3. Pop the TOP node (LIFO)
        
        if problem.is_goal(node): # 4. Check if we won
            return node
            
        # 5. EXPANSION (The Critical Part)
        children = problem.expand(node)
        
        # 6. REVERSE the children before pushing
        # If children are [A, B], reversed is [B, A]
        for child in reversed(children): 
            frontier.append(child)
            # Stack becomes: [..., B, A]
            # Next pop() gets A (Left child), preserving order.
```

**How it runs:**
1.  **Line 1**: Initialize stack. Stack = `[S]`.
2.  **Line 3**: Pop `S`.
3.  **Line 5**: Expand `S`. Neighbors = `[A, B]`.
4.  **Line 6**: We need to visit `A` first. Since it's a stack (LIFO), `A` must be on **TOP**.
    *   We reverse `[A, B]` to `[B, A]`.
    *   Push `B`. Stack = `[B]`.
    *   Push `A`. Stack = `[B, A]`.
5.  **Next Loop**: `pop()` takes `A` (Success! We visit Left child first).

---

### 4.2 Minimax with Alpha-Beta (Q3)

```python
def minimax(game, depth, is_max, alpha, beta):
    # 1. BASE CASE
    if game.check_win(ai): return 10
    if game.check_win(human): return -10
    if game.is_full(): return 0
    
    # 2. MAXIMIZER (AI's Turn)
    if is_max:
        best_score = -infinity         # Start with worst possible score
        for move in game.moves():      # Try every empty square
            game.make_move(move, ai)   # SIMULATE: Place AI piece
            
            # RECURSE: Switch to Minimizer (is_max=False)
            score = minimax(game, depth+1, False, alpha, beta)
            
            game.undo_move(move)       # BACKTRACK: Remove piece
            
            best_score = max(best_score, score) # Pick higher score
            alpha = max(alpha, score)           # Update best guarantee
            
            if beta <= alpha:          # PRUNING
                break                  # Stop looking (Cutoff)
        return best_score

    # 3. MINIMIZER (Human's Turn)
    else:
        best_score = +infinity         # Start with worst score (for min)
        for move in game.moves():
            game.make_move(move, human)# SIMULATE: Place Human piece 
            
            # RECURSE: Switch to Maximizer (is_max=True)
            score = minimax(game, depth+1, True, alpha, beta)
            
            game.undo_move(move)       # BACKTRACK
            
            best_score = min(best_score, score) # Pick lower score
            beta = min(beta, score)             # Update opponent's guarantee
            
            if beta <= alpha:          # PRUNING
                break
        return best_score
```

**How it runs:**
1.  **Simulation**: It actually places a piece on the board (`make_move`). The board state changes.
2.  **Recursion**: It calls itself, but flips the player (`True` -> `False`). It dives deeper and deeper until someone wins or board is full.
3.  **Backtracking**: When the recursion returns, the function continues. It **MUST** remove the piece it placed (`undo_move`) so the board is clean for the next loop iteration.
4.  **Pruning**:
    *   Imagine AI finds a move that leads to a Win (+10). `alpha` becomes 10.
    *   Later, in a different branch, if the Human finds a move that leads to a Loss (-10), `beta` might become -10.
    *   If `beta <= alpha`, we stop. We don't need to know exactly how bad it is, just that it's worse than what we already have ensured elsewhere.

