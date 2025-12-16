# Assignment Requirements

1. **Correction of Depth-First Search (DFS) Error**
   Identify and correct the mistake in the implementation of the **Depth-First Search (DFS)** algorithm, specifically focusing on the **incorrect node position**.

2. **Analysis of Depth-First Search in Adversarial Games**
   Compare and analyze the applicability of **Depth-First Search** in an **adversarial game environment**.
   Explain why DFS **cannot be effectively used** in adversarial games, and contrast it with the **Minimax algorithm**.

   Depth-First Search is suitable for **fully deterministic and predefined problem spaces**, where the outcome of each action is known in advance.

   In contrast, **adversarial games are not fully deterministic**, as the outcome depends on the actions of an opponent whose decisions cannot be predicted in advance.

3. **Minimax Implementation for Tic-Tac-Toe**
   Implement the **Minimax algorithm** for the game **Tic-Tac-Toe**, including:

   * Clear **pseudocode**
   * Explicit **termination (base) conditions** in the recursive function

   **Bonus (10 points):**
   Implement **Alpha–Beta Pruning** to optimize the Minimax algorithm.