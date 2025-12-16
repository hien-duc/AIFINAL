# Question 2: DFS in Adversarial Environments

## 1. Can DFS find an Optimal Path in an Adversarial Game?
**Direct Answer**: **No**, DFS cannot effectively find an optimal path in an adversarial game environment (like Pacman with Ghosts).

*   **Reasoning**: DFS is designed for **deterministic, single-agent** problems where the agent fully controls the outcome of its actions. In an adversarial game, the **opponent (Ghosts)** actively tries to minimize the agent's utility (score).
*   **Pacman Context**: If Pacman uses DFS, he might find a path to a food pellet that goes through a Ghost, thinking "I can move to the food" without realizing the Ghost will move to kill him on the very next turn. DFS blindly searches deep into a "best-case" scenario ignoring the opponent's moves.

## 2. Applicability of DFS in Adversarial Scenarios
**Does it guarantee optimality?**: **No**.

*   DFS is **not applicable** for finding winning strategies in adversarial games because it lacks the **min-max** logic required to handle a hostile opponent.
*   **Optimality**: DFS is not even optimal in single-agent environments (it returns the *first* path found, not the shortest). In adversarial environments, it is even worse because it fails to account for the opponent's optimal play. It essentially hopes the opponent will play poorly.

## 3. Why DFS Cannot Guarantee an Optimal Solution
DFS fails to guarantee an optimal solution in adversarial games for three key reasons:

1.  **Lack of Opponent Modeling (The "Blind Spot")**: DFS assumes that if a sequence of moves $A \rightarrow B \rightarrow C$ exists in the state space, the agent can execute it. In reality, after move $A$, the opponent plays, likely changing the state to something where $B$ is no longer possible or safe.
2.  **Greedy/Depth-First Nature**: DFS commits to a path until it hits a dead end. In games, "dead ends" (losing states) must be avoided at all costs. DFS might explore a losing branch for millions of steps before backtracking, whereas Minimax would prune it immediately upon seeing the opponent has a winning move.
3.  **No Concept of "Value"**: DFS sees states as "Goal" or "Not Goal". It does not assign utility values (like +10 or -100) to intermediate states based on the opponent's best response, which is crucial for games.

---

## 4. Comparison with Minimax (Reference)
As used in Lab 5 (Pacman), **Minimax** is the correct algorithm because:
*   **DFS**: Maximizes its own score assuming no interference.
*   **Minimax**: Maximizes its score assuming the opponent will try to minimize it (Best response to Worst case).

| Feature | DFS | Minimax |
| :--- | :--- | :--- |
| **Opponent** | Ignores opponent. | Models opponent as optimal. |
| **Optimality** | No (First valid path). | Yes (Best utility against optimal play). |
| **Environment** | Static/Deterministic. | Dynamic/Adversarial. |
