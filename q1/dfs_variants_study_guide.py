"""
DFS VARIANTS STUDY GUIDE FOR AI EXAM
====================================
This file contains ~30 variants/cases of DFS implementation that often appear in exams.
Each 'case' function represents a specific implementation choice, bug, or edge case.

Structure:
1.  Standard Implementations (Iterative vs Recursive)
2.  The "Node Position" / Visiting Order Variants (The Prompt Question)
3.  Goal Check Timing Variants
4.  Visited Marking Timing Variants
5.  Edge Case Handling (Cycles, Disconnected)
6.  Return Value Variants
"""

# START: Helper Classes
class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children else []
    def __repr__(self): return self.name

class Problem:
    def __init__(self):
        # A simple graph: S -> [A, B]; A -> [C]; B -> [D]
        self.S = Node('S')
        self.A = Node('A')
        self.B = Node('B')
        self.C = Node('C')
        self.D = Node('D')
        self.S.children = [self.A, self.B]
        self.A.children = [self.C]
        self.B.children = [self.D]
        self.initial = self.S
        self.goal_state = 'D'

    def is_goal(self, node): return node.name == self.goal_state
    def expand(self, node): return node.children

p = Problem()

# ==========================================
# SECTION 1: VISITING ORDER VARIANTS (STACK)
# ==========================================

def case_01_standard_iterative_dfs(problem):
    """CASE 1: Standard Iterative DFS (Right-to-Left visiting).
    Push children in natural order [A, B].
    Stack LIFO: Pop B, then A.
    Result: Visits S -> B -> D ..."""
    stack = [problem.initial]
    visited = set()
    while stack:
        node = stack.pop()
        if node in visited: continue
        visited.add(node)
        if problem.is_goal(node): return node
        # Add children naturally
        for child in problem.expand(node):
            stack.append(child)

def case_02_corrected_iterative_dfs(problem):
    """CASE 2: Corrected Iterative DFS (Left-to-Right visiting).
    Push children in REVERSE order [B, A].
    Stack LIFO: Pop A, then B.
    Result: Visits S -> A -> C ..."""
    stack = [problem.initial]
    visited = set()
    while stack:
        node = stack.pop()
        # ... logic ...
        for child in reversed(problem.expand(node)):
            stack.append(child)

def case_03_sort_alphabetical_dfs(problem):
    """CASE 3: Ordered DFS. 
    Sorts children alphabetically (reversed) to ensure strict alphabetical visiting order."""
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        children = problem.expand(node)
        children.sort(key=lambda x: x.name, reverse=True) # Z-A push -> A-Z pop
        stack.extend(children)

# ==========================================
# SECTION 2: GOAL CHECK TIMING
# ==========================================

def case_04_goal_check_on_pop(problem):
    """CASE 4: Standard. Check goal when node is popped/visited.
    Use this when path cost doesn't matter or heuristic isn't used."""
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        if problem.is_goal(node): return node # Standard
        stack.extend(problem.expand(node))

def case_05_goal_check_on_generation(problem):
    """CASE 5: Early Goal Test (Optimization).
    Check goal BEFORE pushing to stack. Returns faster but be careful with path logic."""
    if problem.is_goal(problem.initial): return problem.initial
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        for child in problem.expand(node):
            if problem.is_goal(child): return child # Early exit
            stack.append(child)

# ==========================================
# SECTION 3: VISITED SET LOGIC (GRAPH VS TREE)
# ==========================================

def case_06_graph_search_proper(problem):
    """CASE 6: Graph Search. Consistently marks visited to prevent cycles."""
    visited = set()
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        if node in visited: continue
        visited.add(node)
        stack.extend(problem.expand(node))

def case_07_tree_search_infinite_loop(problem):
    """CASE 7: Tree Search (Bug in Graphs). 
    No visited set. Will loop forever if graph has cycles (S->A->S)."""
    stack = [problem.initial]
    while stack:
        node = stack.pop() # No visited check
        stack.extend(problem.expand(node))

def case_08_visited_on_push_bug(problem):
    """CASE 8: Mark Visited on Push (Subtle Bug).
    Can prevent finding optimal path in BFS, less critical in DFS but prevents re-visiting nodes via other paths in stack."""
    stack = [problem.initial]
    visited = {problem.initial}
    while stack:
        node = stack.pop()
        for child in problem.expand(node):
            if child not in visited:
                visited.add(child) # Marking here
                stack.append(child)

# ==========================================
# SECTION 4: RECURSIVE VARIANTS
# ==========================================

def case_09_recursive_dfs_standard(node, problem, visited=None):
    """CASE 9: Standard Recursive DFS.
    Implicitly visits Left-to-Right."""
    if visited is None: visited = set()
    if problem.is_goal(node): return node
    visited.add(node)
    for child in problem.expand(node):
        if child not in visited:
            result = case_09_recursive_dfs_standard(child, problem, visited)
            if result: return result
    return None

def case_10_recursive_dfs_postorder(node, problem, visited):
    """CASE 10: Post-Order DFS. Process node AFTER children."""
    visited.add(node)
    for child in problem.expand(node):
        if child not in visited:
            case_10_recursive_dfs_postorder(child, problem, visited)
    print(f"Post-order processing {node}")

# ==========================================
# SECTION 5: DEPTH-LIMITED & IDDFS
# ==========================================

def case_11_dls_recursive(node, problem, limit):
    """CASE 11: Recursive Depth-Limited Search."""
    if problem.is_goal(node): return node
    if limit == 0: return 'cutoff'
    cutoff_occurred = False
    for child in problem.expand(node):
        result = case_11_dls_recursive(child, problem, limit-1)
        if result == 'cutoff': cutoff_occurred = True
        elif result: return result
    return 'cutoff' if cutoff_occurred else 'failure'

def case_12_iddfs(problem, max_depth=100):
    """CASE 12: Iterative Deepening DFS (IDDFS).
    Combines DFS space efficiency with BFS completeness."""
    for depth in range(max_depth):
        result = case_11_dls_recursive(problem.initial, problem, depth)
        if result != 'cutoff': return result # Found or empty

# ==========================================
# SECTION 6: PATH RECONSTRUCTION
# ==========================================

def case_13_dfs_return_path_dictionary(problem):
    """CASE 13: Path via Parent Pointers (Dict).
    Stores where we came from."""
    stack = [problem.initial]
    parents = {problem.initial: None}
    while stack:
        node = stack.pop()
        if problem.is_goal(node):
            # Reconstruct
            path = []
            while node:
                path.append(node)
                node = parents[node]
            return path[::-1]
        for child in problem.expand(node):
            if child not in parents:
                parents[child] = node
                stack.append(child)

def case_14_dfs_stack_of_paths(problem):
    """CASE 14: Stack stores Logic Paths [S, A, C].
    Heavy memory usage but simple logic."""
    stack = [[problem.initial]]
    while stack:
        path = stack.pop()
        node = path[-1]
        if problem.is_goal(node): return path
        for child in problem.expand(node):
            new_path = list(path)
            new_path.append(child)
            stack.append(new_path)

# ==========================================
# SECTION 7: EDGE CASES
# ==========================================

def case_15_start_is_goal(problem):
    """CASE 15: Start is Goal check."""
    if problem.is_goal(problem.initial): return [] # Zero length path
    # ... continue ...

def case_16_disconnected_components(problem, all_nodes):
    """CASE 16: Handling Disconnected Graphs.
    Outer loop to restart DFS on unvisited nodes."""
    visited = set()
    for start_node in all_nodes:
        if start_node not in visited:
            # Run DFS(start_node)
            pass

def case_17_cycle_detection_recursion(node, path_set):
    """CASE 17: Cycle detection in current recursion stack."""
    path_set.add(node)
    for child in node.children:
        if child in path_set:
            print("Cycle detected!")
        else:
            case_17_cycle_detection_recursion(child, path_set)
    path_set.remove(node) # Backtrack

# ==========================================
# SECTION 8: EXAM TRAPS & BUGS
# ==========================================

def case_18_typo_bfs_queue(problem):
    """CASE 18: The 'Accidental BFS' Trap.
    Using pop(0) instead of pop() turns stack into queue."""
    stack = [problem.initial]
    while stack:
        node = stack.pop(0) # BUG: This is BFS now!
        # ...
        
def case_19_forgot_visited_check_on_pop(problem):
    """CASE 19: Lazy Visited Check Missing.
    Adding to stack doesn't check visited, must check on Pop."""
    stack = [problem.initial]
    visited = set()
    while stack:
        node = stack.pop()
        # MISSING: if node in visited: continue
        # RESULT: Redundant processing of same nodes
        visited.add(node)

def case_20_incorrect_depth_check_dls(node, limit):
    """CASE 20: Off-by-one error in DLS limit.
    Checking limit vs depth logic."""
    # if limit < 0: return... vs if limit == 0: return...
    pass

# ==========================================
# SECTION 9: ADVANCED / OBSCURE
# ==========================================

def case_21_bidirectional_search_intent(problem):
    """CASE 21: Bidirectional Search (Not DFS usually, but related).
    DFS from start and Goal? Hard to meet in middle without huge memory."""
    pass

def case_22_non_recursive_dfs_postorder_simulation(problem):
    """CASE 22: Simulating Post-Order Iteratively.
    Complex stack management (peek vs pop)."""
    pass

def case_23_dfs_on_implicit_graph(game_state):
    """CASE 23: Implicit Graph (Game).
    Nodes are generated on fly, not stored in dict."""
    pass

def case_24_dfs_max_depth_guard(problem):
    """CASE 24: Safety Guard DFS.
    Regular DFS but with hard counter to preventing stack overflow."""
    pass

def case_25_yielding_generator_dfs(problem):
    """CASE 25: Generator/Iterator DFS.
    yield node instead of return."""
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        yield node
        # ...

def case_26_dfs_finding_all_paths(problem):
    """CASE 26: Find ALL paths to goal, not just one.
    Don't stop on goal, record and backtrack."""
    pass

def case_27_memory_efficient_visited(problem):
    """CASE 27: BitSet Visited (if nodes are integers)."""
    pass

def case_28_frontier_size_limit(problem):
    """CASE 28: Beam Search variant (Sort of).
    Limit stack size? No, that's beam search."""
    pass

def case_29_topological_sort_dfs(problem):
    """CASE 29: DFS for Topological Sort.
    Prepend node to result list after visiting children."""
    pass

def case_30_kosaraju_scc(problem):
    """CASE 30: Strongly Connected Components.
    Two pass DFS strategy."""
    pass

if __name__ == "__main__":
    print("Loaded 30 variants of DFS for study.")
    # Demonstrate Case 1 vs 2
    print(f"Case 1 (Standard/Reverse Order): {case_01_standard_iterative_dfs(p)}")
    print(f"Case 2 (Corrected/Natural Order): {case_02_corrected_iterative_dfs(p)}")
