# Normal DFS vs. Depth-Limited Search (DLS)

Based on the theory image provided, here is the clear difference between **Normal Depth-First Search (DFS)** and **Depth-Limited Search (DLS)**.

## 1. The Core Difference: "The Stop Sign"

*   **Normal DFS**: Keeps going down a path until it hits a **dead end** (no children) or a node it has **already seen** (cycle).
    *   *Risk*: If the graph is infinite or extremely deep, DFS might never return (Infinite Loop).
*   **Depth-Limited Search (DLS)**: Adds a **Depth Limit ($\ell$)**. It acts like DFS but carries a standard: "If I am deeper than level $\ell$, I stop and turn back, even if there are more nodes."

## 2. Comparison Table

| Feature | Normal DFS | Depth-Limited Search (DLS) |
| :--- | :--- | :--- |
| **Termination** | Stops only at leaf nodes or visited states. | Stops at leaf nodes, visited states, **OR** when `Depth > Limit`. |
| **Infinite Loops** | **High Risk**. Can get stuck going down forever in infinite spaces. | **Safe**. Will guaranteed return once the limit is reached. |
| **Completeness** | **Not Complete** (in infinite spaces). | **Not Complete** (if the solution is deeper than the limit). |
| **Result States** | Returns `Node` or `Failure`. | Returns `Node`, `Failure`, or `Cutoff` (Special state meaning "I stopped because of limit"). |

## 3. Code Difference (Key Line)

The image you provided highlights exactly where DLS differs from DFS.

### Normal DFS Logic
```python
if problem.Goal_Test(node): return node

# DFS just keeps expanding if not a cycle
for child in expand(node):
    stack.push(child)
```

### Depth-Limited Search Logic (From your Image)
```python
if problem.Goal_Test(node): return node

# THE KEY DIFFERENCE:
if Depth(node) > limit:
    result = cutoff  # Stop! Don't add children.
else:
    for child in expand(node):
        stack.push(child)
```

## Summary

## 4. Full Code Implementation

Here is runnable Python code showing both side-by-side.

### 5. Code Matching Your Pseudocode Image (Iterative)

This version strictly follows the structure in your image (using a loop/stack instead of recursion).

```python
import sys

def iterative_deepening_search(problem):
    # function ITERATIVE-DEEPENING-SEARCH(problem)
    # for depth = 0 to infinity
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        # if result != cutoff then return result
        if result != 'cutoff':
            return result

def depth_limited_search(problem, limit):
    # frontier <- a LIFO queue (stack) with NODE(problem.INITIAL)
    # We store (state, depth) to track depth like the pseudocode's NODE structure
    frontier = [(problem.initial, 0)] 
    
    # result <- failure
    result = 'failure'
    
    # while not IS-EMPTY(frontier) do
    while frontier:
        # node <- POP(frontier)
        node, current_depth = frontier.pop()
        
        # if problem.IS-GOAL(node.STATE) then return node
        if problem.is_goal(node):
            return node
            
        # if DEPTH(node) > l then
        if current_depth > limit:
            # result <- cutoff
            result = 'cutoff'
            
        # else if not IS-CYCLE(node) do
        # (Assuming simple graph check or omit for tree)
        else:
            # for each child in EXPAND(problem, node) do
            children = problem.expand(node)
            for child in children:
                # add child to frontier
                frontier.append((child, current_depth + 1))
                
    # return result
    return result
```

### 6. Normal DFS Code (Matching Structure for Comparison)

Here is Normal DFS written **exactly** like the code above, just removing the "Limit" logic. compare them line-by-line!

```python
def depth_first_search(problem):
    # frontier <- a LIFO queue (stack) with NODE(problem.INITIAL)
    # Note: We don't need to store 'depth' anymore!
    frontier = [problem.initial] 
    
    # result <- failure
    result = 'failure'
    
    # while not IS-EMPTY(frontier) do
    while frontier:
        # node <- POP(frontier)
        node = frontier.pop()
        
        # if problem.IS-GOAL(node.STATE) then return node
        if problem.is_goal(node):
            return node
            
        # --- LIMIT CHECK REMOVED HERE ---
        # We don't check depth. We just always expand.
            
        # for each child in EXPAND(problem, node) do
        children = problem.expand(node)
        for child in children:
            # add child to frontier
            frontier.append(child)
                
    # return result
    return result
```
