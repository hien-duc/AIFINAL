"""
DFS NODE POSITION (STACK ORDER) VARIANTS
========================================
10 variants focusing specifically on the "Incorrect Node Position" error.
The core issue is usually: "In what order do I push neighbors to visit them in the desired order?"

Expected Traversal for 'Right-to-Left' (Standard Stack): 
    If neighbors are [A, B], we usually want to pop A then B.
    To pop A first, A must be ON TOP.
    Stack should look like: [B, A].
    So we must push B, then push A. (Reverse order).

"""

class Problem:
    def __init__(self):
        self.initial = 'S'
        self.graph = {'S': ['A', 'B'], 'A': ['C', 'D'], 'B': ['E', 'F']} # Left-to-Right
    def expand(self, node): return self.graph.get(node, [])
    def is_goal(self, node): return False 

# ------------------------------------------------------------------
# VARIANT 1: The "Naive" Bug (Most Common Exam Question)
# ------------------------------------------------------------------
def variant_1_naive_append(problem):
    """
    BUG: Appends children in natural order.
    Stack becomes [A, B]. Pop -> B.
    Result: Visits Right child first. (Incorrect if Left-first is required)
    """
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        print(node, end=' ') 
        for child in problem.expand(node):
            stack.append(child) # [..., A, B]

# ------------------------------------------------------------------
# VARIANT 2: The "Extend" Bug
# ------------------------------------------------------------------
def variant_2_extend_natural(problem):
    """
    BUG: Same as variant 1 but using .extend().
    Stack becomes [A, B]. Pop -> B.
    """
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        print(node, end=' ')
        # .extend adds list to end: [..., A, B]
        stack.extend(problem.expand(node)) 

# ------------------------------------------------------------------
# VARIANT 3: The Correct Logic (Reverse Loop)
# ------------------------------------------------------------------
def variant_3_correct_reverse_loop(problem):
    """
    CORRECT: Pushes B then A.
    Stack becomes [B, A]. Pop -> A.
    Result: Visits Left child first.
    """
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        print(node, end=' ')
        # Reversed: [B, A]
        for child in reversed(problem.expand(node)):
            stack.append(child)

# ------------------------------------------------------------------
# VARIANT 4: The Correct Logic (Sorted Reverse)
# ------------------------------------------------------------------
def variant_4_alphabetical_enforcement(problem):
    """
    CORRECT: Sorts Z->A before pushing, so A is on top.
    Ensures alphabetical visiting regardless of input order.
    """
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        print(node, end=' ')
        children = problem.expand(node)
        # Sort descending (Z, Y, ... B, A)
        children.sort(reverse=True)
        stack.extend(children)

# ------------------------------------------------------------------
# VARIANT 5: The "Queue" Mistake (Accidental BFS)
# ------------------------------------------------------------------
def variant_5_queue_pop_start(problem):
    """
    BUG: Using pop(0) makes it a Queue (BFS).
    "Node position" error becomes "Algorithm Type" error.
    """
    stack = [problem.initial]
    while stack:
        node = stack.pop(0) # BFS!!
        print(node, end=' ')
        for child in problem.expand(node):
            stack.append(child)

# ------------------------------------------------------------------
# VARIANT 6: The "Insert at 0" Mistake (Queue implementation of DFS?)
# ------------------------------------------------------------------
def variant_6_insert_start(problem):
    """
    BUG: Inserting at 0 but popping at end?
    Insert 0 [A, S] -> [B, A, S]? No, complex behavior.
    Usually results in BFS logic if popping from end, or extremely slow array shifts.
    """
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        print(node, end=' ')
        for child in problem.expand(node):
            stack.insert(0, child) # Bad performance, effectively a queue logic relative to pop()

# ------------------------------------------------------------------
# VARIANT 7: Slice Assignment (Correct Logic, Weird Syntax)
# ------------------------------------------------------------------
def variant_7_slice_replacement(problem):
    """
    CORRECT: Replaces top of stack with reversed children.
    Stack manipulation trick.
    """
    stack = [problem.initial]
    while stack:
        node = stack.pop()
        print(node, end=' ')
        children = problem.expand(node)
        # Python list slice assignment
        # Effectively appends reversed list
        stack[len(stack):] = children[::-1]

# ------------------------------------------------------------------
# VARIANT 8: Recursive (Implicit Stack)
# ------------------------------------------------------------------
def variant_8_recursive_natural(node, problem):
    """
    CORRECT (Naturally): Recursion visits first child completely before second.
    Does NOT need reversing.
    Loop: visit(A) -> finishes A -> visit(B).
    """
    print(node, end=' ')
    for child in problem.expand(node):
        variant_8_recursive_natural(child, problem)

# ------------------------------------------------------------------
# VARIANT 9: Recursive (Reversed Bug)
# ------------------------------------------------------------------
def variant_9_recursive_reverse_bug(node, problem):
    """
    BUG: Reversing children in recursion causes Right-to-Left traversal.
    Loop: visit(B) -> finishes B -> visit(A).
    """
    print(node, end=' ')
    for child in reversed(problem.expand(node)):
        variant_9_recursive_reverse_bug(child, problem)

# ------------------------------------------------------------------
# VARIANT 10: Stack with "Visited" Check Bug (Marking too late)
# ------------------------------------------------------------------
def variant_10_visited_position_error(problem):
    """
    BUG: Marking visited *after* expansion or allowing duplicates in stack.
    Result: Nodes added to stack multiple times, processed multiple times.
    """
    stack = [problem.initial]
    visited = set()
    while stack:
        node = stack.pop()
        if node in visited: continue
        # visited.add(node) <--- FORGOT TO MARK HERE (Or marked in expansion loop only behavior)
        print(node, end=' ')
        visited.add(node)
        
        for child in problem.expand(node):
            if child not in visited:
                stack.append(child)

if __name__ == "__main__":
    p = Problem()
    print("Graph: S->[A,B] (Left A, Right B)")
    print("\n1. Naive (Buggy): ", end=''); variant_1_naive_append(p)
    print("\n3. Correct Reverse: ", end=''); variant_3_correct_reverse_loop(p)
    # ... etc
