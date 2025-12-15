# Q2: Analysis of Depth-First Search in Adversarial Games

## 1. Applicability of DFS in Adversarial Games

Depth-First Search (DFS) is a fundamental traversal algorithm used primarily in **single-agent**, **deterministic** environments (like maze solving, pathfinding, or puzzle solving). 

### Why DFS cannot be effectively used in adversarial games:
1.  **Lack of Opponent Modeling**: DFS assumes it controls the environment completely. It searches for a path to a goal state optimally (or sub-optimally) based on its own moves. In an adversarial game (like Chess or Tic-Tac-Toe), the state transition depends on the **opponent's move**, which tries to *prevent* the agent from reaching its goal. DFS has no mechanism to account for a hostile agent minimizing the player's gain.
2.  **Greedy/Blind Nature**: DFS typically explores one path to its depth. If it finds a "winning" state deep down a path, it might assume that path is valid. However, an opponent might simply block that path at the very first step. DFS assumes that *if* a path exists, it can be taken, which is false when another agent dictates half the moves.
3.  **Non-Optimality**: Even if modified, DFS does not naturally find the optimal strategy against an opponent who plays optimally. It processes states in an order (depth-based) that doesn't respect the "Min-Max" value of positions.

## 2. Comparison: DFS vs Minimax

| Feature | Depth-First Search (DFS) | Minimax Algorithm |
| :--- | :--- | :--- |
| **Environment** | Deterministic, Single-Agent (Static) | Adversarial, Multi-Agent (Dynamic/Zero-Sum) |
| **Decision Basis** | Finds *any* path to a goal state. | Finds the *optimal* move assuming optimal opposition. |
| **Transitions** | Controlled entirely by the agent. | Controlled alternately by MAX (agent) and MIN (opponent). |
| **Outcome** | True/False (Found/Not Found) or Path. | Value (Utility Score of the best achievable state). |
| **Graph Type** | Standard State-Space Graph. | Game Tree (AND/OR Graph structure). |

## 3. Deterministic vs Non-Deterministic/Adversarial Contexts

*   **Fully Deterministic Problem Spaces**: As defined in the prompt, these are environments where the outcome of every action is known with certainty (e.g., "Move Right" always moves the agent right). DFS works well here because the "plan" it generates can be executed without interference.
    
*   **Adversarial / Non-Deterministic**: In games, the "outcome" of the player's turn is a state where it is now the *opponent's* turn. The opponent's choice is unknown (non-deterministic from the player's perspective, or adversarial). Minimax addresses this by considering **all possible responses** of the opponent and assuming they will play to minimize the player's score. This "worst-case scenario" planning is what makes Minimax robust for games, whereas DFS fails by hoping for the "best-case" sequence of moves.

## 4. Comparison: DFS vs A* Search

While Minimax is for adversarial games, A* is an informed search algorithm used in deterministic single-agent environments (like DFS), but with significant differences in strategy and performance.

| Feature | Depth-First Search (DFS) | A* Search |
| :--- | :--- | :--- |
| **Type** | **Uninformed (Blind)** Search. Uses only the graph structure. | **Informed (Heuristic)** Search. Uses a heuristic function $h(n)$ to estimate cost to goal. |
| **Strategy** | Explores as deep as possible along each branch before backtracking. Uses logic "LIFO" (Last In, First Out). | Expands the node with the lowest total estimated cost $f(n) = g(n) + h(n)$, where $g(n)$ is cost so far. |
| **Optimality** | **Not Optimal**. Returns the first solution found, which may be a very long path. | **Optimal**. Guaranteed to find the lowest-cost path if the heuristic $h(n)$ is admissible (never overestimates). |
| **Completeness** | Complete only if the search space is finite and has no cycles (or cycle checking is used). Can get stuck in infinite loops. | **Complete**. Will always find a solution if one exists (assuming step costs are valid). |
| **Space Complexity** | **Low**. $O(bm)$ (linear with maximum depth). Only needs to store the current path and unvisited siblings. | **High**. $O(b^d)$ (exponential). Keeps all generated nodes in memory to ensure optimality. |
| **Speed** | Can be faster if the solution is deep and lucky (finds it early). | Generally efficient but overhead of maintaining the priority queue and calculating heuristics can be higher per node. |

**Summary**:
*   Use **DFS** when memory is tight, optimality doesn't matter, or you need to visit every node (like topological sort).
*   Use **A*** when finding the **shortest/optimal path** is critical (e.g., GPS navigation, pathfinding in games).
