"""
DSA Knowledge Base Chunks
Carefully isolated by topic and subtopic to prevent topic contamination during semantic search.
Each chunk contains rich metadata: chunk_id, topic, subtopic, difficulty, problem_name, source, document_name, tags, content.
"""
from typing import Dict, List, Any

DSA_CHUNKS: List[Dict[str, Any]] = [
    # ========================== TREES ==========================
    {
        "chunk_id": "tree-001",
        "topic": "Trees",
        "subtopic": "Binary Tree Fundamentals & Structure",
        "difficulty": "Easy",
        "problem_name": None,
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "binary_trees_fundamentals.md",
        "tags": ["tree", "trees", "binary tree", "root", "leaf", "child", "parent", "depth", "height", "hierarchical"],
        "content": (
            "A tree is a non-linear, hierarchical data structure composed of nodes connected by directed or undirected edges. "
            "The top node is called the Root. Each node contains a value and references (pointers) to its child nodes. "
            "A node with no children is called a Leaf node. In a Binary Tree, each node has at most two children, typically referred "
            "to as the left child and right child. Key properties include: Height (maximum number of edges from root to a leaf), "
            "Depth (number of edges from root to the node), and Size (total number of nodes). "
            "Common binary tree types: Full Binary Tree (every node has 0 or 2 children), Complete Binary Tree (all levels filled except possibly the last, "
            "filled from left to right), and Perfect Binary Tree (all internal nodes have 2 children and all leaves are at the same level)."
        ),
    },
    {
        "chunk_id": "tree-002",
        "topic": "Trees",
        "subtopic": "Binary Tree Traversals (DFS & BFS)",
        "difficulty": "Medium",
        "problem_name": "Binary Tree Level Order Traversal",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "binary_tree_traversals.md",
        "tags": ["tree traversal", "inorder", "preorder", "postorder", "level order", "bfs tree", "dfs tree", "trees"],
        "content": (
            "Binary tree traversals systematically visit every node in a tree. They are divided into Depth-First Search (DFS) and Breadth-First Search (BFS):\n"
            "1. Pre-order (DFS): Visit Root -> Left subtree -> Right subtree. Useful for copying or serializing trees.\n"
            "2. In-order (DFS): Visit Left subtree -> Root -> Right subtree. In a Binary Search Tree (BST), In-order produces elements in strictly sorted ascending order.\n"
            "3. Post-order (DFS): Visit Left subtree -> Right subtree -> Root. Crucial for bottom-up evaluations like calculating tree height, diameter, or deleting nodes.\n"
            "4. Level-order (BFS): Visits nodes level by level from top to bottom, left to right using a FIFO Queue.\n"
            "Time Complexity for all tree traversals is O(N) as each of the N nodes is visited once. Space Complexity is O(H) recursion stack for DFS (where H is tree height, O(log N) balanced, O(N) skewed) and O(W) queue width for BFS."
        ),
    },
    {
        "chunk_id": "tree-003",
        "topic": "Trees",
        "subtopic": "Binary Search Tree (BST) Properties & Operations",
        "difficulty": "Medium",
        "problem_name": "Validate Binary Search Tree",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "binary_search_tree_bst.md",
        "tags": ["bst", "binary search tree", "tree search", "bst validation", "trees", "inorder sorted"],
        "content": (
            "A Binary Search Tree (BST) is a binary tree with the BST ordering invariant: for every node X, all values in its left subtree "
            "are strictly less than X.val (left < X), and all values in its right subtree are strictly greater than X.val (right > X). "
            "Key operations:\n"
            "- Search: Compare target with current node. If target < current, go left; if target > current, go right. Average time O(log N), worst-case O(N) for skewed tree.\n"
            "- Insertion: Traverse to find appropriate null position maintaining invariant, then attach new node. Average O(log N).\n"
            "- Deletion: 3 cases: node has 0 children (remove directly), 1 child (bypass to child), or 2 children (replace with In-order Successor—the smallest node in right subtree—and delete successor).\n"
            "- In-order traversal of a valid BST always yields a strictly monotonically increasing sorted sequence."
        ),
    },
    {
        "chunk_id": "tree-004",
        "topic": "Trees",
        "subtopic": "Lowest Common Ancestor (LCA) in Trees",
        "difficulty": "Medium",
        "problem_name": "Lowest Common Ancestor of a Binary Tree",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "lowest_common_ancestor.md",
        "tags": ["lowest common ancestor", "lca", "binary tree lca", "trees", "post order tree"],
        "content": (
            "The Lowest Common Ancestor (LCA) of two nodes p and q in a tree is the lowest node that has both p and q as descendants. "
            "In a general Binary Tree: Use post-order bottom-up recursion. If the current root is null, p, or q, return root. "
            "Recursively search left subtree and right subtree. If both left and right returns are non-null, the current node is the LCA because p and q lie in different subtrees! "
            "If only one side is non-null, propagate that non-null node upwards. Time complexity is O(N) and space complexity is O(H). "
            "In a BST: We can optimize without full traversal! If both p and q are less than root, LCA lies in left subtree. If both are greater than root, LCA lies in right subtree. "
            "The split point where p <= root <= q is the LCA, taking O(H) time and O(1) iterative space."
        ),
    },

    # ========================== STACK ==========================
    {
        "chunk_id": "stack-001",
        "topic": "Stack",
        "subtopic": "Stack Core Operations (LIFO)",
        "difficulty": "Easy",
        "problem_name": None,
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "stack_fundamentals.md",
        "tags": ["stack", "lifo", "push", "pop", "peek", "call stack", "parentheses"],
        "content": (
            "A Stack is a linear data structure that follows the Last-In, First-Out (LIFO) principle. "
            "The element added most recently is the first one to be removed. "
            "Fundamental operations:\n"
            "- Push: Adds an element to the top of the stack in O(1) time.\n"
            "- Pop: Removes and returns the top element in O(1) time. Throws underflow if empty.\n"
            "- Peek / Top: Inspects the top element without removing it in O(1) time.\n"
            "- isEmpty: Checks if stack contains zero elements in O(1) time.\n"
            "Common applications include: function call recursion stack, undo/redo mechanisms in text editors, syntax parsing, "
            "expression evaluation (Infix to Postfix conversion), and depth-first search (DFS)."
        ),
    },
    {
        "chunk_id": "stack-002",
        "topic": "Stack",
        "subtopic": "Monotonic Stack Pattern & Next Greater Element",
        "difficulty": "Medium",
        "problem_name": "Daily Temperatures",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "monotonic_stack.md",
        "tags": ["monotonic stack", "next greater element", "daily temperatures", "largest rectangle in histogram", "stack"],
        "content": (
            "A Monotonic Stack is a specialized stack where elements are kept in strictly increasing or strictly decreasing order. "
            "It solves range query problems like finding the Next Greater Element, Next Smaller Element, or Previous Greater Element in linear O(N) time instead of O(N^2) brute force.\n"
            "Pattern Logic for Next Greater Element (Monotonically Decreasing Stack):\n"
            "1. Iterate through array elements (or indices).\n"
            "2. While stack is not empty and current element > array[stack.top()], pop the top index! The current element is the Next Greater Element for that popped index.\n"
            "3. Push current index onto the stack.\n"
            "Every element is pushed and popped at most once, guaranteeing amortized O(N) time and O(N) auxiliary space."
        ),
    },
    {
        "chunk_id": "stack-003",
        "topic": "Stack",
        "subtopic": "Parentheses Matching & Syntax Validation",
        "difficulty": "Easy",
        "problem_name": "Valid Parentheses",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "valid_parentheses_stack.md",
        "tags": ["valid parentheses", "matching brackets", "stack bracket", "stack"],
        "content": (
            "Valid Parentheses is the quintessential stack problem. Given a string containing '(', ')', '{', '}', '[', and ']', "
            "determine if the input string has properly matching and nested brackets.\n"
            "Algorithm:\n"
            "1. Initialize an empty stack.\n"
            "2. When encountering an opening bracket ('(', '{', '['), push the corresponding closing bracket onto the stack.\n"
            "3. When encountering a closing bracket, check if the stack is empty (unmatched closing) or if stack.pop() != current character (mismatched type). If so, return false.\n"
            "4. At the end, the string is valid if and only if the stack is completely empty.\n"
            "Time Complexity: O(N) single-pass. Space Complexity: O(N) in worst-case where all characters are opening brackets."
        ),
    },

    # ========================== QUEUE ==========================
    {
        "chunk_id": "queue-001",
        "topic": "Queue",
        "subtopic": "Queue Operations (FIFO) & Circular Queue",
        "difficulty": "Easy",
        "problem_name": None,
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "queue_fundamentals.md",
        "tags": ["queue", "fifo", "enqueue", "dequeue", "circular queue", "deque", "buffer"],
        "content": (
            "A Queue is a linear data structure that follows the First-In, First-Out (FIFO) principle. "
            "The element added first is the first one to be removed (like a line of people waiting).\n"
            "Core operations:\n"
            "- Enqueue (Offer/Push): Adds an element to the rear (tail) of the queue in O(1) time.\n"
            "- Dequeue (Poll/Pop): Removes and returns the element from the front (head) of the queue in O(1) time.\n"
            "- Front / Peek: Inspects the front element without removal in O(1) time.\n"
            "A Circular Queue connects the last position back to the first position using modulo arithmetic: `rear = (rear + 1) % capacity`, avoiding memory waste from continuous dequeues in fixed-size arrays. "
            "A Double-Ended Queue (Deque) permits O(1) insertion and deletion at both ends."
        ),
    },
    {
        "chunk_id": "queue-002",
        "topic": "Queue",
        "subtopic": "Queue Applications: BFS & Buffer Processing",
        "difficulty": "Medium",
        "problem_name": "Implement Queue using Stacks",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "queue_applications_bfs.md",
        "tags": ["queue", "bfs queue", "fifo processing", "queue using stacks", "sliding window maximum"],
        "content": (
            "Queues are critical for systems engineering and algorithm design:\n"
            "1. Breadth-First Search (BFS): Explores nodes in order of their distance from the source. A queue guarantees nodes at distance K are processed before nodes at distance K+1.\n"
            "2. Job Scheduling & Buffering: Asynchronous printer queues, network packet routing, OS CPU task scheduling (round-robin).\n"
            "3. Implementing Queue using Two Stacks: InStack handles pushes in O(1). When popping, if OutStack is empty, transfer all elements from InStack to OutStack (reversing LIFO to FIFO). Amortized O(1) time per operation.\n"
            "4. Monotonic Deque: Maintains candidates for Sliding Window Maximum in O(N) total time by popping smaller elements from the back and out-of-bound elements from the front."
        ),
    },

    # ========================== GRAPHS ==========================
    {
        "chunk_id": "graph-001",
        "topic": "Graphs",
        "subtopic": "Graph Representations & Core Properties",
        "difficulty": "Easy to Medium",
        "problem_name": None,
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "graph_representations.md",
        "tags": ["graph", "graphs", "adjacency list", "adjacency matrix", "directed", "undirected", "weighted"],
        "content": (
            "A Graph G = (V, E) consists of a set of vertices (nodes) V and a set of edges E connecting pairs of vertices. "
            "Graphs can be Directed (edges have specific direction u -> v) or Undirected (bidirectional edges u <-> v), Weighted or Unweighted, Cyclic or Acyclic (DAG).\n"
            "Representations:\n"
            "1. Adjacency List: An array or hash map of lists where `adj[u]` stores all neighbors of vertex u. Space complexity O(V + E). Preferred for sparse graphs (E << V^2).\n"
            "2. Adjacency Matrix: A 2D array of size V x V where `matrix[u][v] = 1` if edge exists. Space complexity O(V^2). Offers O(1) edge lookup, preferred for dense graphs."
        ),
    },
    {
        "chunk_id": "graph-002",
        "topic": "Graphs",
        "subtopic": "Breadth-First Search (BFS) in Graphs",
        "difficulty": "Medium",
        "problem_name": "Shortest Path in Unweighted Graph",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "graph_bfs.md",
        "tags": ["bfs", "breadth first search", "graph bfs", "shortest path", "graphs", "level order"],
        "content": (
            "Breadth-First Search (BFS) explores vertices in concentric layers by distance from the starting source vertex. "
            "It is the gold standard for finding the SHORTEST PATH in unweighted graphs.\n"
            "Algorithm:\n"
            "1. Initialize a FIFO Queue and a `visited` boolean array (or set).\n"
            "2. Enqueue the starting vertex and mark it as visited.\n"
            "3. While queue is not empty, dequeue current vertex u.\n"
            "4. For each unvisited neighbor v of u, mark v as visited and enqueue v.\n"
            "5. Track layer levels to compute shortest distance.\n"
            "Time Complexity: O(V + E) because every vertex is enqueued once and every edge is examined. Space Complexity: O(V) for queue and visited set."
        ),
    },
    {
        "chunk_id": "graph-003",
        "topic": "Graphs",
        "subtopic": "Depth-First Search (DFS) in Graphs",
        "difficulty": "Medium",
        "problem_name": "Number of Islands",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "graph_dfs.md",
        "tags": ["dfs", "depth first search", "graph dfs", "connected components", "cycle detection", "graphs", "recursion"],
        "content": (
            "Depth-First Search (DFS) explores as deep as possible along each branch before backtracking. "
            "It is natural for connectivity, finding connected components, cycle detection, path existence, and maze solving.\n"
            "Algorithm:\n"
            "1. Maintain a `visited` set to prevent infinite loops in cyclic graphs.\n"
            "2. At current vertex u, mark visited.\n"
            "3. Recursively call DFS on every unvisited neighbor of u.\n"
            "4. For 2D grid graphs (e.g. Number of Islands), explore 4 cardinal directions (up, down, left, right), marking visited land cells in-place.\n"
            "Time Complexity: O(V + E) for standard graphs, O(R * C) for grids. Space Complexity: O(V) for call stack in worst-case linear path."
        ),
    },
    {
        "chunk_id": "graph-004",
        "topic": "Graphs",
        "subtopic": "Topological Sort & Kahn's Algorithm",
        "difficulty": "Medium",
        "problem_name": "Course Schedule",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "topological_sort_kahns.md",
        "tags": ["topological sort", "kahn", "course schedule", "dag", "indegree", "cycle detection", "graphs"],
        "content": (
            "Topological Sort produces a linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u -> v, "
            "vertex u appears before vertex v in the ordering. If the graph contains a directed cycle, no topological order exists!\n"
            "Kahn's Algorithm (BFS approach):\n"
            "1. Compute in-degree (number of incoming directed edges) for every vertex.\n"
            "2. Enqueue all vertices with in-degree == 0 into a FIFO queue.\n"
            "3. While queue is not empty, dequeue node u, add u to topological order, and decrement in-degree for all neighbors of u.\n"
            "4. If a neighbor's in-degree becomes 0, enqueue it.\n"
            "5. Cycle Detection: If the count of nodes in the topological order < V, a cycle exists (e.g., circular prerequisites in Course Schedule).\n"
            "Time Complexity: O(V + E). Space Complexity: O(V) for in-degree array and queue."
        ),
    },

    # ========================== BINARY SEARCH ==========================
    {
        "chunk_id": "bs-001",
        "topic": "Binary Search",
        "subtopic": "Binary Search Algorithm & Invariants",
        "difficulty": "Easy to Medium",
        "problem_name": "Binary Search",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "binary_search_fundamentals.md",
        "tags": ["binary search", "search", "sorted array", "log n", "divide and conquer", "midpoint overflow", "search space"],
        "content": (
            "Binary Search is an optimal divide-and-conquer search algorithm for sorted arrays or monotonic answer spaces. "
            "It repeatedly evaluates the middle element and halves the remaining candidate search space.\n"
            "Standard Template:\n"
            "1. Initialize `left = 0`, `right = n - 1`.\n"
            "2. Loop while `left <= right`.\n"
            "3. Compute midpoint: `mid = left + (right - left) // 2` (prevents 32-bit integer overflow instead of `(left + right) / 2`).\n"
            "4. If `nums[mid] == target`, return `mid`.\n"
            "5. If `nums[mid] < target`, target must reside in right half: `left = mid + 1`.\n"
            "6. Else target resides in left half: `right = mid - 1`.\n"
            "7. Return -1 if not found.\n"
            "Time Complexity: O(log N) guaranteed. Space Complexity: O(1) iterative auxiliary space."
        ),
    },
    {
        "chunk_id": "bs-002",
        "topic": "Binary Search",
        "subtopic": "Binary Search on Answer Space Pattern",
        "difficulty": "Medium to Hard",
        "problem_name": "Koko Eating Bananas",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "binary_search_on_answer.md",
        "tags": ["binary search on answer", "koko eating bananas", "aggressive cows", "capacity to ship packages", "binary search", "monotonic predicate"],
        "content": (
            "Binary Search on Answer applies when you need to find the minimum or maximum value X that satisfies a monotonic condition f(X).\n"
            "Monotonicity Property: If speed S is sufficient to finish bananas in time H, any speed > S is also sufficient. "
            "If speed S is insufficient, any speed < S is definitely insufficient.\n"
            "Pattern:\n"
            "1. Define search bounds: `low = 1`, `high = max(piles)`.\n"
            "2. In while loop `low <= high`, test `mid = low + (high - low) // 2` with a helper function `canFinish(mid, H)`.\n"
            "3. If `canFinish(mid, H)` is True: record `mid` as possible answer and try smaller values: `high = mid - 1`.\n"
            "4. If False: speed is too slow, increase search space: `low = mid + 1`.\n"
            "Time Complexity: O(N * log(max_val)) where N is validation cost and log(range) is search space."
        ),
    },

    # ========================== DYNAMIC PROGRAMMING ==========================
    {
        "chunk_id": "dp-001",
        "topic": "Dynamic Programming",
        "subtopic": "DP Principles: Memoization vs Tabulation",
        "difficulty": "Medium",
        "problem_name": "Climbing Stairs",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "dynamic_programming_fundamentals.md",
        "tags": ["dynamic programming", "dp", "memoization", "tabulation", "overlapping subproblems", "optimal substructure", "top down", "bottom up"],
        "content": (
            "Dynamic Programming (DP) solves complex optimization problems by breaking them down into simpler overlapping subproblems with optimal substructure. "
            "Two primary paradigms:\n"
            "1. Top-Down with Memoization: Solve recursively from the original problem down to base cases, caching subproblem results in a hash map or array to avoid redundant computations (converts exponential O(2^N) to polynomial O(N)).\n"
            "2. Bottom-Up with Tabulation: Solve iteratively starting from base cases, filling an array or table sequentially until reaching the desired state. Avoids recursion call stack overhead.\n"
            "3. Space Optimization: If a state `dp[i]` depends only on `dp[i - 1]` and `dp[i - 2]` (e.g. Fibonacci, Climbing Stairs, House Robber), space can be reduced from O(N) to O(1) using two rolling variables."
        ),
    },
    {
        "chunk_id": "dp-002",
        "topic": "Dynamic Programming",
        "subtopic": "Classic DP Archetypes: Knapsack & Coin Change",
        "difficulty": "Medium to Hard",
        "problem_name": "Coin Change",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "dp_knapsack_coin_change.md",
        "tags": ["coin change", "0/1 knapsack", "unbounded knapsack", "dynamic programming", "dp"],
        "content": (
            "Classic DP Patterns:\n"
            "1. 0/1 Knapsack: Given items with weights and values, find maximum value fitting capacity W. Each item can be picked at most once. Recurrence: `dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]])`. Iterate capacity backwards in 1D array.\n"
            "2. Unbounded Knapsack / Coin Change: Items can be chosen infinitely many times. Minimum coins to make amount A: `dp[a] = min(dp[a], dp[a - coin] + 1)` for each coin. Iterate capacity forwards.\n"
            "3. Longest Increasing Subsequence (LIS): `dp[i]` is length of longest increasing subsequence ending at index i. Recurrence: `dp[i] = max(dp[j] + 1)` for all `j < i` where `nums[j] < nums[i]`. O(N^2) dynamic programming, optimizable to O(N log N) using patience sorting with binary search."
        ),
    },

    # ========================== HEAPS ==========================
    {
        "chunk_id": "heap-001",
        "topic": "Heaps",
        "subtopic": "Heap Structure, Properties & Priority Queue",
        "difficulty": "Medium",
        "problem_name": "Kth Largest Element in an Array",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "heap_priority_queue.md",
        "tags": ["heap", "heaps", "priority queue", "min heap", "max heap", "kth largest", "heapify", "top k"],
        "content": (
            "A Binary Heap is a complete binary tree satisfying the Heap Property:\n"
            "- Min-Heap: Parent node value <= all its children's values. The root node holds the minimum element.\n"
            "- Max-Heap: Parent node value >= all its children's values. The root node holds the maximum element.\n"
            "Array Representation: For node at index i: Left child = 2i + 1, Right child = 2i + 2, Parent = (i - 1) // 2.\n"
            "Operations:\n"
            "- Insert (Push): Append element to array and sift-up. Time O(log N).\n"
            "- Extract-Min/Max (Pop): Swap root with last element, pop, and sift-down root. Time O(log N).\n"
            "- Peek: Read root in O(1) time.\n"
            "- Build-Heap (Heapify): Transforms an unordered array of N elements into a valid heap in O(N) time (linear!).\n"
            "Top-K Pattern: To find the Kth largest element in an array of size N, maintain a Min-Heap of size K. Process each element: if heap size > K, pop smallest. The root contains the Kth largest in O(N log K) time and O(K) auxiliary space."
        ),
    },

    # ========================== LINKED LISTS ==========================
    {
        "chunk_id": "ll-001",
        "topic": "Linked Lists",
        "subtopic": "Linked List Pointer Manipulation & Fast/Slow Pointer",
        "difficulty": "Easy to Medium",
        "problem_name": "Reverse Linked List",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "linked_list_patterns.md",
        "tags": ["linked list", "reverse linked list", "fast slow pointer", "floyd cycle detection", "dummy node", "linked lists"],
        "content": (
            "A Linked List is a linear collection of data elements (nodes) where linear order is given by pointers rather than physical memory adjacency.\n"
            "Essential Patterns:\n"
            "1. Dummy Head Node: Eliminates special cases when modifying the list head or merging lists. Return `dummy.next` at the end.\n"
            "2. Reversing a Linked List: Maintain three pointers: `prev = null`, `curr = head`, `next = null`. Iterate: save `next = curr.next`, set `curr.next = prev`, shift `prev = curr`, `curr = next`. Returns `prev` in O(N) time and O(1) space.\n"
            "3. Fast & Slow Pointers (Floyd's Tortoise and Hare):\n"
            "   - Middle of List: `slow` moves 1 step, `fast` moves 2 steps. When `fast` reaches end, `slow` is at midpoint.\n"
            "   - Cycle Detection: If `slow` and `fast` meet, a cycle exists. To find cycle start: reset `slow = head`, advance both by 1 step until they meet."
        ),
    },

    # ========================== ARRAYS & TWO POINTERS ==========================
    {
        "chunk_id": "arr-001",
        "topic": "Arrays",
        "subtopic": "Kadane's Algorithm & Prefix Sums",
        "difficulty": "Medium",
        "problem_name": "Maximum Subarray",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "kadanes_algorithm_prefix_sums.md",
        "tags": ["kadanes algorithm", "kadane", "maximum subarray", "prefix sum", "arrays", "contiguous sum"],
        "content": (
            "Kadane's Algorithm finds the contiguous subarray with the largest sum in a single pass in O(N) time and O(1) space.\n"
            "Core Intuition: At each index i, decide whether to extend the current running subarray sum or start fresh from the current number: "
            "`current_sum = max(nums[i], current_sum + nums[i])`.\n"
            "Keep updating `max_sum = max(max_sum, current_sum)`. Initialize `current_sum = nums[0]` and `max_sum = nums[0]` to correctly handle all-negative arrays.\n"
            "Prefix Sum Pattern: `prefix[i] = prefix[i - 1] + nums[i]`. Allows querying sum of any subarray `[L, R]` in O(1) time: `sum(L, R) = prefix[R] - prefix[L - 1]`. "
            "Combined with a Hash Map storing running prefix frequencies, solves 'Subarray Sum Equals K' in O(N) linear time."
        ),
    },
    {
        "chunk_id": "arr-002",
        "topic": "Two Pointers",
        "subtopic": "Converging & Parallel Pointers Pattern",
        "difficulty": "Medium",
        "problem_name": "Trapping Rain Water",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "two_pointers_pattern.md",
        "tags": ["two pointers", "converging pointers", "palindrome", "trapping rain water", "3sum", "container with most water"],
        "content": (
            "The Two Pointers technique traverses a sequence using two references to avoid O(N^2) nested loops.\n"
            "1. Converging Pointers: Place `left = 0` and `right = n - 1`. Move towards each other based on conditions. Classic for Pair Sum in sorted arrays, checking Palindromes, and Container With Most Water.\n"
            "2. Trapping Rain Water: Maintain `left_max` and `right_max`. Water trapped at bar i is bounded by the shorter wall. Advance the pointer with smaller height: if `height[left] < height[right]`, update `left_max` and accumulate `left_max - height[left]`, then increment `left`. Runs in O(N) time and O(1) space.\n"
            "3. 3Sum: Sort array in O(N log N). Fix element i, then use two pointers on `[i + 1, n - 1]` to find pairs summing to `-nums[i]`. Skip duplicates to prevent duplicate triplets in O(N^2) time."
        ),
    },
    {
        "chunk_id": "arr-003",
        "topic": "Sliding Window",
        "subtopic": "Fixed & Dynamic Sliding Window Pattern",
        "difficulty": "Medium",
        "problem_name": "Longest Substring Without Repeating Characters",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "sliding_window_pattern.md",
        "tags": ["sliding window", "fixed window", "dynamic window", "longest substring", "contiguous sequence"],
        "content": (
            "Sliding Window optimizes contiguous sequence processing from O(N^2) to O(N) by maintaining window boundaries `[left, right]`.\n"
            "1. Fixed Window: Window size K remains constant. Add element entering on right, subtract element leaving on left. Time O(N).\n"
            "2. Dynamic Window: Expand `right` pointer to include elements. When constraint is violated (e.g., character repeats, or sum exceeds target), shrink from `left` until valid again.\n"
            "For 'Longest Substring Without Repeating Characters': Use a hash map storing `char -> last_seen_index`. When character is repeated at index `j`, jump `left = max(left, last_seen[char] + 1)`. Calculate `max_len = max(max_len, right - left + 1)`. Amortized O(N) time and O(min(N, Alphabet_Size)) space."
        ),
    },

    # ========================== HASHING ==========================
    {
        "chunk_id": "hash-001",
        "topic": "Hashing",
        "subtopic": "Hash Maps, Hash Sets & Two Sum Pattern",
        "difficulty": "Easy to Medium",
        "problem_name": "Two Sum",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "hashing_fundamentals.md",
        "tags": ["hash map", "hashing", "hash table", "hash set", "two sum", "frequency count", "collision"],
        "content": (
            "A Hash Map (Hash Table) maps keys to values using a Hash Function, delivering average O(1) time complexity for insertion, lookup, and deletion. "
            "Collisions are resolved via Chaining (linked lists or balanced trees per bucket) or Open Addressing (linear/quadratic probing).\n"
            "Key DSA Applications:\n"
            "1. Two Sum Complement Pattern: For each number x, check if `(target - x)` exists in hash map. If present, return pair indices; otherwise store `seen[x] = i`. Reduces O(N^2) brute force to O(N) time and O(N) space.\n"
            "2. Frequency Counting: Counting frequencies of elements for Anagram detection, Top K Frequent elements, and Majority Element.\n"
            "3. Constant Time Set Membership: Using Hash Set to test existence in O(1) average time."
        ),
    },

    # ========================== RECURSION & BACKTRACKING ==========================
    {
        "chunk_id": "bt-001",
        "topic": "Backtracking",
        "subtopic": "Backtracking Paradigm & State Space Tree",
        "difficulty": "Medium to Hard",
        "problem_name": "Subsets & N-Queens",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "backtracking_fundamentals.md",
        "tags": ["backtracking", "recursion", "subsets", "permutations", "n-queens", "state space tree", "pruning"],
        "content": (
            "Backtracking is an algorithmic paradigm that systematically explores all candidate solutions by building candidates incrementally "
            "and abandoning ('backtracking' from) candidates that cannot lead to a valid final solution.\n"
            "Standard Backtracking Template:\n"
            "```python\ndef backtrack(start_index, current_state):\n    if is_solution(current_state):\n        result.append(list(current_state))\n        return\n    for choice in valid_choices(start_index):\n        current_state.append(choice)      # 1. CHOOSE\n        backtrack(next_index, current_state) # 2. EXPLORE\n        current_state.pop()               # 3. UNCHOOSE (backtrack)\n```\n"
            "Pruning: Check bounding conditions early (e.g., if sum exceeds target) to trim branches of the decision tree, dramatically improving average runtime."
        ),
    },

    # ========================== SORTING ==========================
    {
        "chunk_id": "sort-001",
        "topic": "Sorting",
        "subtopic": "Merge Sort & Quick Sort Divide-and-Conquer",
        "difficulty": "Medium",
        "problem_name": "Sort an Array",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "merge_sort_quick_sort.md",
        "tags": ["sorting", "merge sort", "quick sort", "divide and conquer", "quicksort", "mergesort", "stable sort"],
        "content": (
            "Merge Sort and Quick Sort are divide-and-conquer sorting algorithms:\n"
            "1. Merge Sort: Recursively divides array into two equal halves, sorts them, and merges sorted halves using two pointers.\n"
            "   - Time Complexity: O(N log N) in best, average, and worst cases (guaranteed!).\n"
            "   - Space Complexity: O(N) auxiliary space for the merge buffer.\n"
            "   - Stability: Stable (maintains relative order of equal elements).\n"
            "2. Quick Sort: Picks a pivot element, partitions the array such that elements < pivot go to left and elements > pivot go to right, then recursively sorts partitions.\n"
            "   - Time Complexity: O(N log N) average, O(N^2) worst case (avoidable with randomized pivot selection).\n"
            "   - Space Complexity: O(log N) auxiliary recursion stack.\n"
            "   - In-place partitioning makes Quick Sort cache-friendly and faster in practice for primitive arrays."
        ),
    },

    # ========================== TRIES ==========================
    {
        "chunk_id": "trie-001",
        "topic": "Trie",
        "subtopic": "Prefix Tree Design & Autocomplete",
        "difficulty": "Medium",
        "problem_name": "Implement Trie (Prefix Tree)",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "trie_prefix_tree.md",
        "tags": ["trie", "prefix tree", "autocomplete", "string matching", "prefix search"],
        "content": (
            "A Trie (Prefix Tree) is a specialized tree structure used for storing associative arrays where keys are strings. "
            "Each node represents a character. Edges connect successive characters in words. A boolean flag `is_end` marks word termination.\n"
            "Key Advantages:\n"
            "- Insert word of length L in O(L) time.\n"
            "- Search word of length L in O(L) time.\n"
            "- Prefix Search: Find all words starting with prefix P in O(|P|) time, independent of dictionary size N!\n"
            "Hash tables require O(L) to search a full word but cannot efficiently query prefixes without iterating over all stored words."
        ),
    },

    # ========================== BIT MANIPULATION ==========================
    {
        "chunk_id": "bit-001",
        "topic": "Bit Manipulation",
        "subtopic": "Bitwise Operations & Brian Kernighan's Algorithm",
        "difficulty": "Easy to Medium",
        "problem_name": "Single Number",
        "source": "AlgoMentor Curated DSA Knowledge Base",
        "document_name": "bit_manipulation_tricks.md",
        "tags": ["bit manipulation", "bitwise", "xor", "count set bits", "single number", "power of two"],
        "content": (
            "Bitwise operations manipulate numbers directly at the binary bit level in O(1) time and O(1) space.\n"
            "Key Bitwise Tricks:\n"
            "1. XOR Properties: `x ^ 0 = x`, `x ^ x = 0`. Associative and commutative. Finding the Single Number among pairs: XOR all numbers together; pairs cancel out leaving the unique number.\n"
            "2. Clear lowest set bit: `n & (n - 1)`. Unsets the rightmost 1-bit. Used in Brian Kernighan's algorithm to count set bits in O(number of set bits) iterations.\n"
            "3. Power of Two Check: `n > 0 and (n & (n - 1)) == 0`. A power of two has exactly one set bit.\n"
            "4. Get / Set / Clear bit k: Get: `(n >> k) & 1`. Set: `n | (1 << k)`. Clear: `n & ~(1 << k)`."
        ),
    },
]


def get_all_chunks() -> List[Dict[str, Any]]:
    return DSA_CHUNKS
