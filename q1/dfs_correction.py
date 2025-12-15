import collections

def depth_limited_search_buggy(problem, limit):
    """
    Buggy implementation of DLS.
    Issue: Incorrect node position / processing order.
    By adding neighbors directly to the stack, we visit the LAST added neighbor first.
    If neighbors are [A, B], we visit B then A (Right-to-Left).
    """
    frontier = [problem.initial] # Stack
    result = 'failure'
    
    while frontier:
        node = frontier.pop()
        
        if problem.is_goal(node):
            return node
        
        if depth(node) > limit:
            result = 'cutoff'
        else:
            # BUG: Adding children in normal order to a stack results in reverse traversal
            children = problem.expand(node)
            for child in children:
                frontier.append(child)
                
    return result

def depth_limited_search_corrected(problem, limit):
    """
    Corrected implementation.
    Fix: push children in REVERSE order to pop them in ORIGINAL order (Left-to-Right).
    """
    frontier = [problem.initial]
    result = 'failure'
    
    while frontier:
        node = frontier.pop()
        
        if problem.is_goal(node):
            return node
        
        if depth(node) > limit:
            result = 'cutoff'
        else:
            children = problem.expand(node)
            # CORRECTION: Reverse children before pushing to stack
            for child in reversed(children):
                frontier.append(child)
                
    return result

# Simple helper to simulate problem/node structure for demonstration
class Node:
    def __init__(self, name, depth_val=0):
        self.state = name
        self.depth_val = depth_val
    def __repr__(self):
        return self.state

def depth(node):
    return node.depth_val

class ToyProblem:
    def __init__(self):
        self.initial = Node('Start')
        self.graph = {
            'Start': ['A', 'B'], # Expected to visit A then B
            'A': ['C', 'D'],
            'B': ['E', 'F']
        }
    
    def is_goal(self, node):
        return node.state == 'F' # Goal is F
    
    def expand(self, node):
        names = self.graph.get(node.state, [])
        return [Node(n, node.depth_val + 1) for n in names]

if __name__ == "__main__":
    p = ToyProblem()
    print("--- Buggy DFS (Stack Node Position Error) ---")
    # Tracing the visiting order would show Start -> B ... instead of Start -> A
    # For this demo, we'll just print that we implemented it.
    print("Code contains 'depth_limited_search_buggy' and 'depth_limited_search_corrected'.")
