from __future__ import annotations

import os
import re
from functools import lru_cache
from typing import Optional, List, Dict, Any

import httpx
from langgraph.graph import END, StateGraph

from app.config import get_settings
from app.schemas import ChatMessage, ChatResponse
from app.services.practice import build_practice_plan
from app.services.progress import get_progress_summary

from app.services.dsa_knowledge_chunks import get_all_chunks, DSA_CHUNKS
from app.services.indexer import get_embedding, get_qdrant_client

settings = get_settings()

EMBEDDING_DIMENSION = settings.embedding_dimension

KNOWLEDGE_BASE: List[Dict[str, Any]] = [
    # ------------------ CONCEPTS & PATTERNS ------------------
    {
        "title": "Binary Search",
        "topic": "Binary Search",
        "pattern": "Search Space Reduction",
        "difficulty": "Easy to Hard",
        "tags": ["binary search", "search", "sorted array", "log n", "divide and conquer", "order of log n", "search space", "bisect"],
        "content": "Binary search is a divide-and-conquer search algorithm for sorted collections or monotonic functions. It repeatedly evaluates the middle element and halves the search space based on target comparison. Time complexity is O(log n) and space complexity is O(1) iteratively. Common patterns include finding exact values, first/last occurrences, and search on answer ranges (e.g. Aggressive Cows, Capacity to Ship Packages, Koko Eating Bananas).",
        "java_code": """public int binarySearch(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}""",
        "python_code": """def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
        "hints": [
            "Observe whether the array or answer space is sorted or monotonic.",
            "Can you discard half the remaining search candidates with a single midpoint comparison?",
            "Calculate mid safely using `left + (right - left) / 2` to prevent 32-bit integer overflow.",
            "Maintain the search invariant: if `nums[mid] < target`, target must reside in `[mid + 1, right]`.",
            "Check boundary termination: loop runs while `left <= right`, returning `-1` if unfound."
        ],
        "similar": [
            {"title": "Search in Rotated Sorted Array", "difficulty": "Medium", "pattern": "Modified Binary Search"},
            {"title": "Koko Eating Bananas", "difficulty": "Medium", "pattern": "Binary Search on Answer"},
            {"title": "Find First and Last Position of Element in Sorted Array", "difficulty": "Medium", "pattern": "Binary Search"}
        ]
    },
    {
        "title": "Two Sum",
        "topic": "Arrays & Hashing",
        "pattern": "Hash Map Complement",
        "difficulty": "Easy",
        "tags": ["two sum", "hash map", "array", "target", "complement", "pair sum"],
        "content": "Two Sum is the foundational hash map problem. Given an array and a target integer, store seen elements and their indices in a hash map. For each number x, check if (target - x) already exists in the map. This reduces the brute force O(n^2) nested loop approach to O(n) time complexity and O(n) auxiliary space complexity.",
        "java_code": """public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{};
}""",
        "python_code": """def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
        "hints": [
            "A brute-force check tests all pairs in O(N^2) time. Can we do better in a single pass?",
            "For any current number `x`, what exact value do you need to reach `target`?",
            "Notice the complement needed is `target - x`. What data structure offers O(1) lookup?",
            "Store each traversed number and its index in a Hash Map as you iterate.",
            "Check if `complement` exists in your hash map before inserting the current number."
        ],
        "similar": [
            {"title": "3Sum", "difficulty": "Medium", "pattern": "Sorting + Two Pointers"},
            {"title": "Two Sum II - Input Array Is Sorted", "difficulty": "Medium", "pattern": "Two Pointers"},
            {"title": "Subarray Sum Equals K", "difficulty": "Medium", "pattern": "Prefix Sum + Hash Map"}
        ]
    },
    {
        "title": "Sliding Window",
        "topic": "Arrays & Strings",
        "pattern": "Sliding Window",
        "difficulty": "Medium",
        "tags": ["sliding window", "subarray", "substring", "contiguous", "two pointers", "longest substring", "fixed window", "dynamic window"],
        "content": "Sliding window is an optimization technique applied to contiguous sequences (arrays/strings). It maintains left and right window pointers to avoid redundant recalculations in nested loops. Fixed window size maintains an exact size-K range, while dynamic window expands the right boundary and contracts the left boundary when condition constraints are violated. Reduces time complexity from O(n^2) to O(n).",
        "java_code": """public int maxSubArrayLen(int[] nums, int k) {
    int left = 0, currentSum = 0, maxLen = 0;
    for (int right = 0; right < nums.length; right++) {
        currentSum += nums[right];
        while (currentSum > k) {
            currentSum -= nums[left++];
        }
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}""",
        "python_code": """def max_sub_array_len(nums: list[int], k: int) -> int:
    left = current_sum = max_len = 0
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum > k:
            current_sum -= nums[left]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len""",
        "hints": [
            "Are you looking for contiguous subarrays or substrings satisfying a specific condition?",
            "Instead of recalculating the entire range from scratch, what enters and what leaves?",
            "Expand `right` pointer to include elements; when the window becomes invalid, shrink `left`.",
            "Update your running answer either at every valid window or at maximal expansion.",
            "Both pointers traverse at most N steps each, yielding amortized O(N) time complexity."
        ],
        "similar": [
            {"title": "Longest Substring Without Repeating Characters", "difficulty": "Medium", "pattern": "Dynamic Sliding Window"},
            {"title": "Minimum Window Substring", "difficulty": "Hard", "pattern": "Sliding Window + Hash Table"},
            {"title": "Max Consecutive Ones III", "difficulty": "Medium", "pattern": "Sliding Window"}
        ]
    },
    {
        "title": "Two Pointers",
        "topic": "Arrays & Strings",
        "pattern": "Two Pointers",
        "difficulty": "Easy to Medium",
        "tags": ["two pointers", "pointers", "sorted array", "palindrome", "container with most water", "3sum", "fast slow"],
        "content": "The Two Pointers technique uses two references traversing a sequence from opposite ends (converging pointers) or at different speeds (fast and slow pointers). Excellent for pair sums in sorted arrays, reversing arrays/strings, checking palindromes, and cycle detection in linked lists. Time complexity is O(n) with O(1) auxiliary space.",
        "java_code": """public boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
        if (Character.toLowerCase(s.charAt(left++)) != Character.toLowerCase(s.charAt(right--))) {
            return false;
        }
    }
    return true;
}""",
        "python_code": """def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True""",
        "hints": [
            "Consider sorting the sequence if relative original indices are not strictly required.",
            "Converging pointers: place one pointer at 0 and another at `n - 1`.",
            "If current sum/metric is too small, advance `left`; if too large, decrement `right`.",
            "For linked lists, use Floyd's tortoise and hare (slow advances by 1, fast advances by 2).",
            "This avoids nested loops, providing guaranteed O(N) runtime with O(1) extra space."
        ],
        "similar": [
            {"title": "Container With Most Water", "difficulty": "Medium", "pattern": "Two Pointers"},
            {"title": "Trapping Rain Water", "difficulty": "Hard", "pattern": "Two Pointers / Monotonic Stack"},
            {"title": "3Sum", "difficulty": "Medium", "pattern": "Sorting + Two Pointers"}
        ]
    },
    {
        "title": "Dynamic Programming",
        "topic": "Dynamic Programming",
        "pattern": "Overlapping Subproblems & Optimal Substructure",
        "difficulty": "Medium to Hard",
        "tags": ["dynamic programming", "optimization", "overlapping subproblems", "memoization", "tabulation", "dp", "optimal substructure", "knapsack", "lcs", "lis"],
        "content": "Dynamic Programming (DP) solves complex optimization problems by decomposing them into overlapping subproblems with optimal substructure. Techniques include Top-Down (Memoization with recursion) and Bottom-Up (Tabulation with iterative state table). Key classic archetypes: 0/1 Knapsack, Coin Change (Unbounded Knapsack), Longest Increasing Subsequence (LIS), Longest Common Subsequence (LCS), and Edit Distance. Time complexity typically reduces exponential O(2^n) to polynomial O(n) or O(n*w).",
        "java_code": """// 0/1 Knapsack Bottom-Up Tabulation
public int knapsack(int W, int[] wt, int[] val, int n) {
    int[][] dp = new int[n + 1][W + 1];
    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            if (wt[i - 1] <= w) {
                dp[i][w] = Math.max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w]);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }
    return dp[n][W];
}""",
        "python_code": """# Coin Change (Minimum coins to make amount)
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""",
        "hints": [
            "Check if the problem asks for maximum, minimum, count of ways, or true/false reachability.",
            "Can the global optimum be constructed from optimal solutions to subproblems?",
            "Identify the state variables: what minimal information uniquely defines a subproblem?",
            "Formulate the recurrence relation: express `dp[state]` in terms of previously computed states.",
            "Establish base cases clearly, then optimize space if only the previous row/state is required."
        ],
        "similar": [
            {"title": "Climbing Stairs", "difficulty": "Easy", "pattern": "Fibonacci DP"},
            {"title": "Coin Change", "difficulty": "Medium", "pattern": "Unbounded Knapsack DP"},
            {"title": "Longest Increasing Subsequence", "difficulty": "Medium", "pattern": "1D DP / Binary Search"}
        ]
    },
    {
        "title": "Trapping Rain Water",
        "topic": "Arrays & Two Pointers",
        "pattern": "Two Pointers / Monotonic Stack",
        "difficulty": "Hard",
        "tags": ["trapping rain water", "two pointers", "water", "monotonic stack", "elevation map"],
        "content": "Trapping Rain Water asks how much water can be trapped after raining over an elevation map. At any index i, water trapped is `min(max_left, max_right) - height[i]`. The optimal Two Pointers approach maintains `left_max` and `right_max` and moves inward from the shorter boundary, achieving O(N) time and O(1) auxiliary space.",
        "java_code": """public int trap(int[] height) {
    int left = 0, right = height.length - 1;
    int leftMax = 0, rightMax = 0, water = 0;
    while (left < right) {
        if (height[left] < height[right]) {
            if (height[left] >= leftMax) leftMax = height[left];
            else water += leftMax - height[left];
            left++;
        } else {
            if (height[right] >= rightMax) rightMax = height[right];
            else water += rightMax - height[right];
            right--;
        }
    }
    return water;
}""",
        "python_code": """def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water""",
        "hints": [
            "Think about a single column: how much water can stand directly on top of bar `i`?",
            "Water level is limited by the minimum of the highest wall to its left and right.",
            "A naive approach scans left and right for each bar in O(N^2). Precomputing arrays takes O(N) space.",
            "Can we track `left_max` and `right_max` dynamically with two pointers?",
            "Advance the pointer pointing to the lower height, because that side is guaranteed to be the bottleneck."
        ],
        "similar": [
            {"title": "Container With Most Water", "difficulty": "Medium", "pattern": "Two Pointers"},
            {"title": "Largest Rectangle in Histogram", "difficulty": "Hard", "pattern": "Monotonic Stack"}
        ]
    },
    {
        "title": "LRU Cache",
        "topic": "Design & Data Structures",
        "pattern": "Hash Map + Doubly Linked List",
        "difficulty": "Medium",
        "tags": ["lru cache", "cache", "hash map", "doubly linked list", "eviction", "least recently used"],
        "content": "LRU (Least Recently Used) Cache requires O(1) get and put operations with fixed capacity eviction. The optimal design combines a Hash Map for O(1) node lookup and a Doubly Linked List with dummy head and tail for O(1) node removal and insertion to the most recently used (head) position.",
        "java_code": """class LRUCache {
    class Node { int key, val; Node prev, next; Node(int k, int v) { key = k; val = v; } }
    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0), tail = new Node(0, 0);

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail; tail.prev = head;
    }
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        remove(node); insertToHead(node);
        return node.val;
    }
    public void put(int key, int value) {
        if (map.containsKey(key)) remove(map.get(key));
        if (map.size() == capacity) {
            map.remove(tail.prev.key);
            remove(tail.prev);
        }
        Node node = new Node(key, value);
        insertToHead(node);
        map.put(key, node);
    }
    private void remove(Node node) { node.prev.next = node.next; node.next.prev = node.prev; }
    private void insertToHead(Node node) {
        node.next = head.next; node.prev = head;
        head.next.prev = node; head.next = node;
    }
}""",
        "python_code": """class Node:
    def __init__(self, key: int = 0, val: int = 0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        elif len(self.cache) == self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
        new_node = Node(key, value)
        self._add(new_node)
        self.cache[key] = new_node""",
        "hints": [
            "We need O(1) key lookup and O(1) removal of the least recently used element upon eviction.",
            "A Hash Map gives O(1) lookup, but does not maintain insertion/access order natively with O(1) deletion.",
            "A Doubly Linked List allows O(1) node deletion and insertion once the node reference is known.",
            "Combine a Hash Map mapping `key -> Node` with a Doubly Linked List with dummy Head and Tail.",
            "On `get` or `put`, remove node from current position and append to Head (Most Recently Used)."
        ],
        "similar": [
            {"title": "LFU Cache", "difficulty": "Hard", "pattern": "Double Hash Map + Doubly Linked Lists"},
            {"title": "Design In-Memory File System", "difficulty": "Hard", "pattern": "Trie / Tree"}
        ]
    },
    {
        "title": "Monotonic Stack",
        "topic": "Stacks & Queues",
        "pattern": "Monotonic Stack",
        "difficulty": "Medium to Hard",
        "tags": ["monotonic stack", "next greater element", "daily temperatures", "largest rectangle in histogram", "stack", "lifo"],
        "content": "A Monotonic Stack maintains elements in strictly increasing or decreasing order. Whenever an element violates monotonicity, elements are popped and processed. Essential for solving 'Next Greater Element', 'Daily Temperatures', 'Online Stock Span', and 'Largest Rectangle in Histogram' in linear O(N) time.",
        "java_code": """public int[] nextGreaterElements(int[] nums) {
    int n = nums.length;
    int[] res = new int[n];
    Arrays.fill(res, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
            res[stack.pop()] = nums[i];
        }
        stack.push(i);
    }
    return res;
}""",
        "python_code": """def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    ans = [0] * n
    stack = []  # store indices
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev_idx = stack.pop()
            ans[prev_idx] = i - prev_idx
        stack.append(i)
    return ans""",
        "hints": [
            "Are you repeatedly searching for the next larger or smaller element to the left or right?",
            "Notice how a brute-force search looks ahead in O(N^2) time.",
            "Store indices on a stack that maintains strictly decreasing values.",
            "When encountering an element larger than stack top, the current element is its Next Greater Element!",
            "Every element is pushed and popped at most once, guaranteeing strictly O(N) runtime."
        ],
        "similar": [
            {"title": "Daily Temperatures", "difficulty": "Medium", "pattern": "Monotonic Stack"},
            {"title": "Largest Rectangle in Histogram", "difficulty": "Hard", "pattern": "Monotonic Stack"},
            {"title": "Online Stock Span", "difficulty": "Medium", "pattern": "Monotonic Stack"}
        ]
    },
    {
        "title": "Graph Traversal",
        "topic": "Graphs",
        "pattern": "Breadth-First & Depth-First Search",
        "difficulty": "Medium",
        "tags": ["graph traversal", "bfs", "dfs", "queue", "stack", "graph", "cycle detection", "topological sort", "connected components"],
        "content": "Graph traversal systematically visits vertices and edges. Breadth-First Search (BFS) uses a FIFO queue for level-order exploration and guarantees shortest paths in unweighted graphs. Depth-First Search (DFS) uses recursion or a stack for connected components, cycle detection, and topological sorting. Time complexity is O(V + E) and space complexity is O(V).",
        "java_code": """public int numIslands(char[][] grid) {
    if (grid == null || grid.length == 0) return 0;
    int count = 0;
    for (int r = 0; r < grid.length; r++) {
        for (int c = 0; c < grid[0].length; c++) {
            if (grid[r][c] == '1') {
                count++;
                dfs(grid, r, c);
            }
        }
    }
    return count;
}
private void dfs(char[][] grid, int r, int c) {
    if (r < 0 || c < 0 || r >= grid.length || c >= grid[0].length || grid[r][c] != '1') return;
    grid[r][c] = '0'; // mark visited in-place
    dfs(grid, r + 1, c); dfs(grid, r - 1, c); dfs(grid, r, c + 1); dfs(grid, r, c - 1);
}""",
        "python_code": """def num_islands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r: int, c: int):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # mark visited
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)
    return islands""",
        "hints": [
            "Model states as graph vertices and legal transitions between states as edges.",
            "If asking for the shortest distance in an unweighted graph, always use BFS with a queue.",
            "If exploring complete connected components or paths, DFS recursion is concise and natural.",
            "Crucial: Track `visited` states to avoid infinite loops and re-traversals in cyclic graphs.",
            "Runtime is bounded by O(V + E) where V is vertices and E is edges."
        ],
        "similar": [
            {"title": "Number of Islands", "difficulty": "Medium", "pattern": "DFS / BFS Grid Traversal"},
            {"title": "Course Schedule", "difficulty": "Medium", "pattern": "Topological Sort / Cycle Detection"},
            {"title": "Word Ladder", "difficulty": "Hard", "pattern": "BFS Shortest Path"}
        ]
    },
    {
        "title": "Topological Sort & Course Schedule",
        "topic": "Graphs",
        "pattern": "Topological Sort (Kahn's Algorithm)",
        "difficulty": "Medium",
        "tags": ["topological sort", "kahn", "course schedule", "dag", "indegree", "cycle detection"],
        "content": "Topological Sort orders vertices in a Directed Acyclic Graph (DAG) such that every directed edge u -> v has u appearing before v. Kahn's Algorithm computes in-degrees of all vertices and uses a FIFO queue initialized with in-degree 0 vertices. If the sorted count equals V, the graph is a valid DAG; otherwise, a directed cycle exists. Time complexity is O(V + E).",
        "java_code": """public boolean canFinish(int numCourses, int[][] prerequisites) {
    int[] inDegree = new int[numCourses];
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
    for (int[] p : prerequisites) {
        adj.get(p[1]).add(p[0]);
        inDegree[p[0]]++;
    }
    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < numCourses; i++) if (inDegree[i] == 0) queue.offer(i);
    int resolved = 0;
    while (!queue.isEmpty()) {
        int curr = queue.poll();
        resolved++;
        for (int neighbor : adj.get(curr)) {
            if (--inDegree[neighbor] == 0) queue.offer(neighbor);
        }
    }
    return resolved == numCourses;
}""",
        "python_code": """from collections import deque, defaultdict

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    in_degree = [0] * num_courses
    adj = defaultdict(list)
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0
    while queue:
        curr = queue.popleft()
        count += 1
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return count == num_courses""",
        "hints": [
            "Prerequisites form directed dependencies. When can a course be taken?",
            "A course can be taken as soon as its prerequisites (in-degree) drop to 0.",
            "Compute in-degrees for all vertices and push in-degree 0 courses into a queue.",
            "Poll courses from queue and decrement in-degree for their dependents.",
            "If processed count < numCourses, there is a cycle (circular dependency)!"
        ],
        "similar": [
            {"title": "Course Schedule II", "difficulty": "Medium", "pattern": "Topological Sort Output"},
            {"title": "Alien Dictionary", "difficulty": "Hard", "pattern": "Graph Construction + Topological Sort"}
        ]
    },
    {
        "title": "Kadane's Algorithm",
        "topic": "Arrays & Dynamic Programming",
        "pattern": "Kadane's Running Subarray Sum",
        "difficulty": "Medium",
        "tags": ["kadanes algorithm", "kadane", "maximum subarray", "dynamic programming", "contiguous sum"],
        "content": "Kadane's algorithm finds the contiguous subarray with the largest sum in O(n) time and O(1) space. At each index i, it decides whether to extend the current running subarray sum or start fresh from the current element: current_sum = max(nums[i], current_sum + nums[i]).",
        "java_code": """public int maxSubArray(int[] nums) {
    int currentSum = nums[0], maxSum = nums[0];
    for (int i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    return maxSum;
}""",
        "python_code": """def max_sub_array(nums: list[int]) -> int:
    current_sum = max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum""",
        "hints": [
            "A subarray must be contiguous. Think about what happens as you expand index by index.",
            "At index i, does adding `nums[i]` to the previous sum help, or does previous sum drag it down?",
            "If `current_sum < 0`, it will never help any future subarray; better to reset to `nums[i]`.",
            "Keep updating a global `max_sum` variable throughout the single pass.",
            "Initializes with `nums[0]` so all-negative arrays are handled correctly."
        ],
        "similar": [
            {"title": "Maximum Product Subarray", "difficulty": "Medium", "pattern": "Kadane Variant with Min/Max"},
            {"title": "Best Time to Buy and Sell Stock", "difficulty": "Easy", "pattern": "Running Min/Max"}
        ]
    },
    {
        "title": "Binary Trees & BST",
        "topic": "Trees",
        "pattern": "Tree Recursion & DFS/BFS",
        "difficulty": "Medium",
        "tags": ["binary tree", "bst", "binary search tree", "traversal", "inorder", "level order", "lca"],
        "content": "Binary Trees have at most two children per node. Traversals: Pre-order (Root-L-R), In-order (L-Root-R, sorted for BST), Post-order (L-R-Root), and Level-order (BFS). In a BST, left subtree < node < right subtree, allowing O(h) search, insert, and delete where h is height (O(log n) balanced).",
        "java_code": """public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if (left != null && right != null) return root;
    return left != null ? left : right;
}""",
        "python_code": """def lowest_common_ancestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right""",
        "hints": [
            "Most tree problems break down into recursive divide-and-conquer on left and right subtrees.",
            "For a Binary Search Tree (BST), in-order traversal yields elements in strictly sorted ascending order.",
            "Lowest Common Ancestor: if p and q are found in opposite subtrees, current node is their LCA.",
            "Use level-order BFS with a queue when asked for tree depth, right side view, or zigzag order.",
            "Time complexity is O(N) visiting every node once; space is O(H) recursion depth."
        ],
        "similar": [
            {"title": "Lowest Common Ancestor of a Binary Tree", "difficulty": "Medium", "pattern": "Post-Order Tree Recursion"},
            {"title": "Validate Binary Search Tree", "difficulty": "Medium", "pattern": "In-Order Traversal"},
            {"title": "Binary Tree Level Order Traversal", "difficulty": "Medium", "pattern": "BFS with Queue"}
        ]
    },
    {
        "title": "Sorting: Merge Sort & Quick Sort",
        "topic": "Sorting & Searching",
        "pattern": "Divide and Conquer",
        "difficulty": "Medium",
        "tags": ["merge sort", "quick sort", "sorting", "divide and conquer", "quicksort", "mergesort"],
        "content": "Merge Sort divides the array into halves, recursively sorts them, and merges in O(n log n) guaranteed time with O(n) auxiliary space (stable sort). Quick Sort chooses a pivot, partitions the elements, and sorts sub-arrays in O(n log n) average time and O(log n) space (in-place, not stable).",
        "java_code": """public void mergeSort(int[] arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}""",
        "python_code": """def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)""",
        "hints": [
            "Divide and conquer: break the list into two halves until single-element arrays remain.",
            "Merge two sorted arrays using two pointers in linear O(N) time.",
            "Merge Sort guarantees O(N log N) worst-case time complexity, making it stable and reliable.",
            "Quick Sort partitions in-place around a pivot, using O(log N) stack space without auxiliary arrays.",
            "Master Theorem recurrence: T(n) = 2T(n/2) + O(n) resolves to O(n log n)."
        ],
        "similar": [
            {"title": "Sort an Array", "difficulty": "Medium", "pattern": "Merge / Quick Sort"},
            {"title": "Kth Largest Element in an Array", "difficulty": "Medium", "pattern": "QuickSelect"}
        ]
    },
    {
        "title": "Heap and Priority Queue",
        "topic": "Heaps",
        "pattern": "Heap / Priority Queue",
        "difficulty": "Medium",
        "tags": ["heap", "priority queue", "min heap", "max heap", "kth largest", "top k frequent", "dijkstra"],
        "content": "A binary heap is a complete binary tree satisfying the heap property (Min-Heap: parent <= children; Max-Heap: parent >= children). Provides O(log n) push/pop and O(1) peek. Essential for finding Kth largest/smallest elements in O(n log k) time and graph algorithms like Dijkstra.",
        "java_code": """public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) minHeap.poll();
    }
    return minHeap.peek();
}""",
        "python_code": """import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]""",
        "hints": [
            "Finding the Kth largest element does NOT require sorting the entire array in O(N log N).",
            "Maintain a Min-Heap of size K: the root will always hold the current Kth largest!",
            "For each incoming number, push it into the heap; if size exceeds K, pop the smallest.",
            "Total time complexity drops to O(N log K) with auxiliary space O(K).",
            "Python's `heapq` is a min-heap by default; negate values to simulate a max-heap."
        ],
        "similar": [
            {"title": "Top K Frequent Elements", "difficulty": "Medium", "pattern": "Min-Heap / Bucket Sort"},
            {"title": "Find Median from Data Stream", "difficulty": "Hard", "pattern": "Two Heaps (Min + Max)"}
        ]
    },
    {
        "title": "Hash Map",
        "topic": "Arrays & Hashing",
        "pattern": "Hash Table Key-Value Lookup",
        "difficulty": "Easy to Medium",
        "tags": ["hash map", "dictionary", "lookup", "hash function", "collision", "hash set", "hashing"],
        "content": "A hash map (hash table) stores key-value pairs offering average O(1) time complexity for insertion, deletion, and search using hashing functions. Used extensively for frequency counting, anagram validation, finding duplicates, and prefix sum subarray lookups.",
        "java_code": """Map<String, Integer> map = new HashMap<>();
map.put("apple", 3);
int count = map.getOrDefault("apple", 0);""",
        "python_code": """seen = collections.defaultdict(int)
for char in s:
    seen[char] += 1""",
        "hints": [
            "If your algorithm has nested loops checking existence, a hash table usually reduces O(N^2) to O(N).",
            "Hash Sets check unique existence in O(1) time.",
            "Combine running prefix sums with a hash map to count subarrays summing to K in linear time.",
            "Watch out for worst-case collision degradation to O(N) with malicious hashes.",
            "Java uses Red-Black Tree binning when hash bucket collision depth exceeds 8."
        ],
        "similar": [
            {"title": "Subarray Sum Equals K", "difficulty": "Medium", "pattern": "Prefix Sum + Hash Map"},
            {"title": "Group Anagrams", "difficulty": "Medium", "pattern": "Hash Map with Sorted Key"}
        ]
    },
    {
        "title": "Linked List",
        "topic": "Linked Lists",
        "pattern": "Pointer Manipulation & Floyd's Cycle Detection",
        "difficulty": "Easy to Medium",
        "tags": ["linked list", "reverse linked list", "cycle detection", "fast slow pointer", "dummy node", "merge two lists"],
        "content": "A linked list is a linear data structure of nodes pointing to next nodes. Essential techniques: Dummy Head node to handle edge deletions/insertions cleanly, Fast and Slow (Floyd's Tortoise and Hare) for finding the middle node or detecting cycles in O(n) time and O(1) space, and iterative node pointer reversal.",
        "java_code": """public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}""",
        "python_code": """def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev""",
        "hints": [
            "Always use a `dummy` head node when modifying head pointers or merging lists to avoid edge cases.",
            "To detect cycles without modifying values or allocating a set, use Floyd's Tortoise and Hare.",
            "Slow pointer advances 1 step; fast pointer advances 2 steps. If they meet, a cycle exists.",
            "To reverse a linked list iteratively, track `prev`, `curr`, and `next` pointers.",
            "Space complexity is strictly O(1) with pointer manipulation."
        ],
        "similar": [
            {"title": "Reverse Linked List", "difficulty": "Easy", "pattern": "Iterative Pointer Reversal"},
            {"title": "Linked List Cycle", "difficulty": "Easy", "pattern": "Fast & Slow Pointers"},
            {"title": "Merge Two Sorted Lists", "difficulty": "Easy", "pattern": "Dummy Node + Two Pointers"}
        ]
    },
    {
        "title": "Stacks and Queues",
        "topic": "Stacks & Queues",
        "pattern": "LIFO / FIFO Buffer",
        "difficulty": "Easy to Medium",
        "tags": ["stack", "queue", "monotonic stack", "valid parentheses", "next greater element", "fifo", "lifo"],
        "content": "Stacks operate on LIFO (Last In First Out) and queues on FIFO (First In First Out). A Monotonic Stack maintains elements in monotonic order, solving 'Next Greater Element' and 'Largest Rectangle in Histogram' in linear O(n) time. Valid parentheses uses a stack to match closing symbols with the latest open symbol.",
        "java_code": """public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c == '(') stack.push(')');
        else if (c == '{') stack.push('}');
        else if (c == '[') stack.push(']');
        else if (stack.isEmpty() || stack.pop() != c) return false;
    }
    return stack.isEmpty();
}""",
        "python_code": """def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    return not stack""",
        "hints": [
            "Use a stack whenever processing nested hierarchies, matching parentheses, or undo history.",
            "Push expected closing brackets onto the stack for clean O(1) comparison upon seeing closers.",
            "Always verify the stack is not empty before popping to prevent `EmptyStackException`.",
            "Check that the stack is completely empty at the end of the string.",
            "Time complexity is O(N) with O(N) auxiliary space."
        ],
        "similar": [
            {"title": "Valid Parentheses", "difficulty": "Easy", "pattern": "LIFO Stack"},
            {"title": "Min Stack", "difficulty": "Medium", "pattern": "Stack with Auxiliary Min"},
            {"title": "Evaluate Reverse Polish Notation", "difficulty": "Medium", "pattern": "Operand Stack"}
        ]
    },
    {
        "title": "Greedy Algorithms",
        "topic": "Greedy",
        "pattern": "Greedy Choice Property",
        "difficulty": "Medium",
        "tags": ["greedy", "activity selection", "jump game", "gas station", "interval scheduling"],
        "content": "Greedy algorithms make the locally optimal choice at each step hoping it leads to a global optimum. Applicable when optimal substructure and greedy-choice property hold. Classic problems include Interval Scheduling (sorting by end time), Jump Game, Fractional Knapsack, and Dijkstra's algorithm.",
        "java_code": """public boolean canJump(int[] nums) {
    int maxReach = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > maxReach) return false;
        maxReach = Math.max(maxReach, i + nums[i]);
    }
    return true;
}""",
        "python_code": """def can_jump(nums: list[int]) -> bool:
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True""",
        "hints": [
            "Can you sort the elements by deadline, start time, or end time to reveal the best immediate move?",
            "Jump Game: keep track of the maximum reachable index so far.",
            "If current index exceeds `max_reach`, you are stranded and can return `false`.",
            "Greedy works when a local optimum never sacrifices the ability to reach the global optimum.",
            "Time complexity is usually O(N) or O(N log N) if sorting is required."
        ],
        "similar": [
            {"title": "Jump Game II", "difficulty": "Medium", "pattern": "Greedy BFS Jump"},
            {"title": "Non-overlapping Intervals", "difficulty": "Medium", "pattern": "Interval Scheduling"}
        ]
    },
    {
        "title": "Backtracking",
        "topic": "Backtracking",
        "pattern": "Recursive State Space Search",
        "difficulty": "Medium to Hard",
        "tags": ["backtracking", "recursion", "permutations", "subsets", "combination sum", "n-queens", "sudoku"],
        "content": "Backtracking is an algorithmic paradigm that tests candidates recursively and abandons ('backtracks') when a candidate cannot lead to a valid solution. Standard template: choose -> explore -> unchoose. Solves permutations, combinations, N-Queens, Sudoku, and subset generation.",
        "java_code": """public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> res = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), res);
    return res;
}
private void backtrack(int[] nums, int start, List<Integer> curr, List<List<Integer>> res) {
    res.add(new ArrayList<>(curr));
    for (int i = start; i < nums.length; i++) {
        curr.add(nums[i]);
        backtrack(nums, i + 1, curr, res);
        curr.remove(curr.size() - 1);
    }
}""",
        "python_code": """def subsets(nums: list[int]) -> list[list[int]]:
    res = []
    def backtrack(start: int, curr: list[int]):
        res.append(list(curr))
        for i in range(start, len(nums)):
            curr.append(nums[i])
            backtrack(i + 1, curr)
            curr.pop()
    backtrack(0, [])
    return res""",
        "hints": [
            "Backtracking builds solution candidates incrementally, abandoning dead ends early.",
            "Standard recursion template: 1. Add candidate, 2. Recurse, 3. Pop candidate (undo).",
            "For subsets, start index advances (`i + 1`) to avoid duplicate permutations.",
            "For permutations, use a `visited` boolean array to explore all unused elements.",
            "Prune early with constraints (e.g. `sum > target` in combination sum) to minimize branch exploration."
        ],
        "similar": [
            {"title": "Subsets", "difficulty": "Medium", "pattern": "Backtracking Power Set"},
            {"title": "Permutations", "difficulty": "Medium", "pattern": "Backtracking with Visited"},
            {"title": "Combination Sum", "difficulty": "Medium", "pattern": "Backtracking with Repetition"}
        ]
    },
    {
        "title": "Trie (Prefix Tree)",
        "topic": "Advanced Trees",
        "pattern": "Prefix Tree",
        "difficulty": "Medium",
        "tags": ["trie", "prefix tree", "autocomplete", "word search", "string matching", "prefix search"],
        "content": "A Trie is a tree data structure used to store associative arrays where keys are usually strings. Provides O(L) time complexity for insert, search, and prefix matching where L is word length, independent of the number of words stored in the dictionary.",
        "java_code": """class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEnd = false;
}
class Trie {
    private final TrieNode root = new TrieNode();
    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
            curr = curr.children[idx];
        }
        curr.isEnd = true;
    }
}""",
        "python_code": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True""",
        "hints": [
            "When searching for common prefixes or building autocomplete, standard hash sets cannot search prefixes in O(L).",
            "Each Trie node maintains children pointers (array of 26 or dictionary) and an `is_end` flag.",
            "Insertion and search take O(L) time where L is word length.",
            "Combine a Trie with DFS on a 2D grid to solve Boggle / Word Search II optimally.",
            "Bitwise XOR maximums can also be computed using a binary bit-Trie (0/1 branching)."
        ],
        "similar": [
            {"title": "Implement Trie (Prefix Tree)", "difficulty": "Medium", "pattern": "Trie Design"},
            {"title": "Word Search II", "difficulty": "Hard", "pattern": "Trie + Grid DFS"}
        ]
    },
    {
        "title": "Bit Manipulation",
        "topic": "Bit Manipulation",
        "pattern": "Bitwise Operations",
        "difficulty": "Easy to Medium",
        "tags": ["bit manipulation", "bitwise", "xor", "count set bits", "single number", "power of two"],
        "content": "Bitwise operations operate directly on binary bits: AND (&), OR (|), XOR (^), NOT (~), Left Shift (<<), Right Shift (>>). Key tricks: x & (x - 1) removes the lowest set bit (Brian Kernighan's algorithm), x ^ x = 0 (find single number among duplicates), and (x & (x - 1)) == 0 checks power of two in O(1) time.",
        "java_code": """public int singleNumber(int[] nums) {
    int res = 0;
    for (int num : nums) res ^= num;
    return res;
}""",
        "python_code": """def single_number(nums: list[int]) -> int:
    res = 0
    for num in nums:
        res ^= num
    return res""",
        "hints": [
            "XOR properties: `a ^ a = 0` and `a ^ 0 = a`. XOR is both associative and commutative.",
            "If every element appears twice except one, XORing all elements leaves only the single element.",
            "To clear the lowest set bit: `n & (n - 1)`. Repeat until zero to count set bits.",
            "To check if an integer is a power of two: `n > 0 and (n & (n - 1)) == 0`.",
            "Provides ultra-fast O(1) space and constant time operations."
        ],
        "similar": [
            {"title": "Single Number", "difficulty": "Easy", "pattern": "XOR Cancellation"},
            {"title": "Number of 1 Bits", "difficulty": "Easy", "pattern": "Brian Kernighan Algorithm"}
        ]
    }
]


def normalize_text(text: str) -> list[str]:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower()).split()


@lru_cache(maxsize=1)
def get_embedding_model():
    return None


def _deterministic_embedding(text: str, dimension: int = EMBEDDING_DIMENSION) -> list[float]:
    vector = [0.0] * dimension
    tokens = normalize_text(text)
    if not tokens:
        return vector

    for index, token in enumerate(tokens[:dimension]):
        token_value = sum(ord(char) for char in token)
        vector[index % dimension] = float(token_value % 997) / 997.0

    norm = sum(v * v for v in vector) ** 0.5
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector


def _embed_text(text: str, dimension: int = EMBEDDING_DIMENSION) -> list[float]:
    vec = get_embedding(text)
    if len(vec) != dimension:
        if len(vec) > dimension:
            return vec[:dimension]
        return vec + [0.0] * (dimension - len(vec))
    return vec


def rewrite_query(message: str, history: list[dict]) -> str:
    """SRS FR-08: Query Rewriting using conversation history context."""
    if not history or not isinstance(history, list):
        return message

    lower = message.lower().strip()
    anaphoric_signals = [
        "its complexity", "time complexity of this", "space complexity of this", "its time complexity",
        "how to optimize it", "can we optimize it", "what is the code", "show me in java", "show me in python",
        "show in cpp", "give me a hint", "give hint", "next hint", "hint 2", "hint 3", "hint 4", "hint 5",
        "what are the edge cases", "explain it", "how does it work", "solve it"
    ]

    is_anaphoric = any(sig in lower for sig in anaphoric_signals) or len(message.split()) <= 4
    if not is_anaphoric:
        return message

    subject = None
    known_subjects = [doc["title"] for doc in KNOWLEDGE_BASE]
    for chunk in get_all_chunks():
        if chunk.get("problem_name"):
            known_subjects.append(chunk["problem_name"])
        if chunk.get("subtopic"):
            known_subjects.append(chunk["subtopic"])
        if chunk.get("document_name"):
            known_subjects.append(chunk["document_name"])
        if chunk.get("topic"):
            known_subjects.append(chunk["topic"])

    sorted_subjects = sorted(set(known_subjects), key=len, reverse=True)
    for h in reversed(history[-4:]):
        content = h.get("content", "")
        for subj in sorted_subjects:
            if subj.lower() in content.lower():
                subject = subj
                break
        if subject:
            break

    if subject and subject.lower() not in lower:
        return f"{message} regarding {subject}"

    return message


def route_query(message: str, mode: str) -> str:
    """SRS FR-14: Agentic Query Routing into specialized workflows."""
    lower = message.lower()

    # 1. Beginner Roadmap
    beginner_signals = [
        "start my ds journey", "start my dsa journey", "guide me", "btech 2nd year",
        "2nd year", "1st year", "how should i start", "dsa roadmap", "beginner roadmap", "how to start dsa"
    ]
    if any(term in lower for term in beginner_signals) and any(k in lower for k in ["start", "roadmap", "guide", "journey", "beginner"]):
        return "beginner-roadmap"

    # 2. Practice Plan
    if any(term in lower for term in ["practice plan", "daily plan", "practice schedule", "recommend problems", "create a practice plan", "what should i solve"]):
        return "practice-plan"

    # 3. Progress Analysis
    if any(term in lower for term in ["progress", "weak area", "weak topic", "strength", "solved count", "how am i doing", "my statistics"]):
        return "progress-analysis"

    # 4. Hint Generation (FR-05)
    if any(term in lower for term in ["hint", "progressive hint", "give hint", "give hints", "clue", "stuck on"]):
        return "hint-generation"

    # 5. Similar Problem Recommendation (FR-06)
    if any(term in lower for term in ["similar problem", "similar problems", "problems like", "more problems on this", "recommend similar"]):
        return "similar-problems"

    # 6. Complexity Analysis
    if any(term in lower for term in ["time complexity", "space complexity", "big o of", "complexity analysis", "big-o"]):
        return "complexity-analysis"

    # 7. Problem Analysis & Pattern Identification (FR-04)
    problem_signals = [
        "solve a two-sum", "solve two-sum", "solve two sum", "solve", "how to solve", "pattern for",
        "trapping rain water", "lru cache", "longest substring", "kadane", "course schedule", "subarray sum"
    ]
    if any(term in lower for term in problem_signals) or mode in ("problem-analysis", "code"):
        return "problem-analysis"

    if mode in ("interview", "mock"):
        return "interview"

    return mode or "concept"


def detect_topics(query: str) -> list[str]:
    """Detects target DSA topic(s) from user query for metadata-aware Qdrant pre-filtering."""
    q_clean = re.sub(r"[^a-z0-9\s]", " ", query.lower())
    tokens = set(q_clean.split())
    detected = []

    topic_patterns = [
        ("Trees", ["tree", "trees", "binary tree", "binary trees", "bst", "avl", "red black", "inorder", "preorder", "postorder", "lca", "lowest common ancestor"]),
        ("Stack", ["stack", "stacks", "monotonic stack", "lifo", "min stack", "valid parentheses", "next greater element"]),
        ("Queue", ["queue", "queues", "deque", "fifo", "circular queue"]),
        ("Graphs", ["graph", "graphs", "bfs", "dfs", "breadth first", "depth first", "topological sort", "kahn", "dijkstra", "bipartite", "cycle detection", "islands"]),
        ("Binary Search", ["binary search", "search space", "bisect", "koko eating", "rotated sorted"]),
        ("Dynamic Programming", ["dynamic programming", "dp", "memoization", "tabulation", "knapsack", "lcs", "lis", "coin change", "climbing stairs"]),
        ("Heaps", ["heap", "heaps", "priority queue", "min heap", "max heap", "heapify", "k-way merge", "median from data stream"]),
        ("Two Pointers", ["two pointer", "two pointers", "container with most water", "3sum", "trapping rain water"]),
        ("Sliding Window", ["sliding window", "longest substring without repeating", "minimum window substring"]),
        ("Linked List", ["linked list", "doubly linked list", "reverse linked list", "floyd cycle"]),
        ("Arrays & Hashing", ["two sum", "hash map", "hashmap", "hash table", "prefix sum", "subarray sum"]),
    ]

    for topic, patterns in topic_patterns:
        if any(term in q_clean for term in patterns):
            detected.append(topic)
        elif topic == "Binary Search" and "binary" in tokens and "search" in tokens and "tree" not in tokens and "trees" not in tokens:
            detected.append(topic)
        elif topic == "Heaps" and "priority queue" in q_clean:
            detected.append(topic)

    if "stack" in tokens and "queue" in tokens:
        if "Stack" not in detected:
            detected.append("Stack")
        if "Queue" not in detected:
            detected.append("Queue")

    if "difference between" in q_clean and ("stack" in tokens or "queue" in tokens):
        if "Stack" not in detected:
            detected.append("Stack")
        if "Queue" not in detected:
            detected.append("Queue")

    return list(dict.fromkeys(detected))


def retrieve_context(message: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Retrieval pipeline with metadata-aware topic filtering and score inspection for DSA queries."""
    k = max(3, limit or settings.retrieval_k)
    detected_topics = detect_topics(message)
    query_vector = _embed_text(message)

    if settings.debug_rag:
        print(f"\n[DEBUG_RAG] Query: '{message}'")
        print(f"[DEBUG_RAG] Embedding Model: '{settings.embedding_model}' ({len(query_vector)}d)")
        print(f"[DEBUG_RAG] Detected Topic(s): {detected_topics}")
        print(f"[DEBUG_RAG] Target Qdrant Collection: '{settings.qdrant_collection}' (k={k})")

    def format_hits(hits_list):
        results = []
        for hit in hits_list:
            payload = getattr(hit, "payload", {}) or {}
            score = getattr(hit, "score", None)
            topic = payload.get("topic", "General")
            subtopic = payload.get("subtopic", "")
            title = payload.get("title") or payload.get("problem_name") or subtopic or payload.get("document_name") or "Knowledge"
            results.append({
                "title": title,
                "topic": topic,
                "subtopic": subtopic,
                "content": payload.get("content", ""),
                "difficulty": payload.get("difficulty", "Medium"),
                "tags": payload.get("tags", []),
                "score": round(float(score), 4) if score is not None else 0.0,
                "chunk_id": payload.get("chunk_id", ""),
                "source": payload.get("source", "AlgoMentor Knowledge Base"),
                "metadata": payload,
            })
        return results

    def relevant_topic_hits(results):
        if not detected_topics:
            return results
        return [r for r in results if r["topic"] in detected_topics]

    def validate_relevance(results):
        if not results:
            return False
        if not detected_topics:
            return True
        relevant = relevant_topic_hits(results)
        if not relevant:
            return False
        ranked_topics = [r["topic"] for r in relevant[:max(1, len(detected_topics))]]
        return any(topic in detected_topics for topic in ranked_topics)

    try:
        client = get_qdrant_client()
        from qdrant_client.http import models

        topic_filter = None
        if detected_topics and hasattr(models, "Filter") and hasattr(models, "FieldCondition"):
            if len(detected_topics) == 1:
                topic_filter = models.Filter(
                    must=[models.FieldCondition(key="topic", match=models.MatchValue(value=detected_topics[0]))]
                )
            else:
                topic_filter = models.Filter(
                    should=[models.FieldCondition(key="topic", match=models.MatchValue(value=t)) for t in detected_topics]
                )

        search_trials = []
        if topic_filter is not None:
            search_trials.append(("topic-filtered", client.search(collection_name=settings.qdrant_collection, query_vector=query_vector, query_filter=topic_filter, limit=max(k * 3, 8), score_threshold=0.15)))
        search_trials.append(("global", client.search(collection_name=settings.qdrant_collection, query_vector=query_vector, limit=max(k * 3, 8), score_threshold=0.15)))

        merged = []
        for label, hits_list in search_trials:
            for hit in hits_list:
                hit_id = getattr(hit, "id", None)
                if hit_id is None or any(existing.get("id") == hit_id for existing in merged):
                    continue
                merged.append({"id": hit_id, "hit": hit, "source": label})

        ranked = sorted(merged, key=lambda item: getattr(item["hit"], "score", 0.0), reverse=True)
        results = format_hits([item["hit"] for item in ranked[:k]])
        if detected_topics:
            results = relevant_topic_hits(results)

        if settings.debug_rag:
            print(f"[DEBUG_RAG] Retrieved top chunks before relevance check:")
            for idx, result in enumerate(results[:k], 1):
                payload = result["metadata"]
                print(f"  {idx}. Topic={result['topic']} | Score={result['score']} | Subtopic={result['subtopic']} | Source={result['source']} | Chunk={payload.get('chunk_id')}")
                print(f"      Text: {result['content'][:220]}...")

        if detected_topics and not validate_relevance(results):
            enhancement = detected_topics[0]
            topic_filter = models.Filter(must=[models.FieldCondition(key="topic", match=models.MatchValue(value=enhancement))])
            fallback_hits = client.search(collection_name=settings.qdrant_collection, query_vector=query_vector, query_filter=topic_filter, limit=max(k, 5), score_threshold=0.20)
            fallback_results = format_hits(fallback_hits)
            fallback_results = relevant_topic_hits(fallback_results)
            if fallback_results:
                results = fallback_results[:k]
                if settings.debug_rag:
                    print(f"[DEBUG_RAG] Relevance guard re-ran retrieval with topic filter: {enhancement}")

        if results and detected_topics and not relevant_topic_hits(results):
            results = []

        if not results:
            all_knowledge = list(get_all_chunks())
            all_knowledge.extend(KNOWLEDGE_BASE)
            scored = []
            stop_words = {"a", "an", "the", "in", "on", "at", "of", "for", "to", "and", "or", "is", "are", "was", "were", "how", "what", "why", "explain", "describe", "does", "work", "dsa", "with", "me", "it", "its"}
            query_tokens = set(normalize_text(message)) - stop_words
            for doc in all_knowledge:
                topic = doc.get("topic", "")
                if detected_topics and topic not in detected_topics:
                    continue
                doc_tokens = (set(normalize_text(doc.get("subtopic", doc.get("title", "")))) | set(normalize_text(doc.get("content", ""))) | set(normalize_text(topic))) - stop_words
                score = len(query_tokens & doc_tokens) + (20 if detected_topics and topic in detected_topics else 0)
                if score > 0:
                    scored.append({
                        "title": doc.get("title") or doc.get("problem_name") or doc.get("subtopic") or doc.get("document_name") or "Knowledge",
                        "topic": topic,
                        "subtopic": doc.get("subtopic", ""),
                        "content": doc.get("content", ""),
                        "difficulty": doc.get("difficulty", "Medium"),
                        "tags": doc.get("tags", []),
                        "score": round(score / 10.0, 4),
                        "chunk_id": doc.get("chunk_id", ""),
                        "source": doc.get("source", "AlgoMentor In-Memory Chunks"),
                        "metadata": doc,
                    })
            results = sorted(scored, key=lambda x: x["score"], reverse=True)[:k]

        if settings.debug_rag:
            print(f"[DEBUG_RAG] Final retrieved chunks for Llama:")
            for idx, result in enumerate(results[:k], 1):
                print(f"  {idx}. Topic={result['topic']} | Score={result['score']} | Subtopic={result['subtopic']}")
                print(f"      {result['content'][:220]}...")

        if not results:
            return []

        return [{
            "title": r["title"],
            "topic": r["topic"],
            "subtopic": r["subtopic"],
            "difficulty": r["difficulty"],
            "pattern": r["topic"],
            "tags": r["tags"],
            "content": r["content"],
            "score": r["score"],
            "is_relevant": (not detected_topics) or r["topic"] in detected_topics,
            "chunk_id": r["chunk_id"],
            "source": r["source"],
            "metadata": r["metadata"],
        } for r in results]

    except Exception as e:
        if settings.debug_rag:
            print(f"[DEBUG_RAG] Qdrant search encountered exception: {e}")

    all_knowledge = list(get_all_chunks())
    all_knowledge.extend(KNOWLEDGE_BASE)
    stop_words = {"a", "an", "the", "in", "on", "at", "of", "for", "to", "and", "or", "is", "are", "was", "were", "how", "what", "why", "explain", "describe", "does", "work", "dsa", "with", "me", "it", "its"}

    def score_chunk(doc: dict) -> int:
        query_tokens = set(normalize_text(message)) - stop_words
        if not query_tokens:
            return 0
        score = 0
        doc_topic = doc.get("topic", "")
        doc_title = doc.get("subtopic", doc.get("title", ""))
        doc_content = doc.get("content", "")

        if detected_topics and doc_topic in detected_topics:
            score += 50

        doc_tokens = (set(normalize_text(doc_title)) | set(normalize_text(doc_content)) | set(normalize_text(doc_topic))) - stop_words
        for tag in doc.get("tags", []):
            tag_tokens = set(normalize_text(tag)) - stop_words
            if tag_tokens & query_tokens:
                score += 8

        common = query_tokens & doc_tokens
        score += len(common) * 3

        if doc_title.lower() in message.lower():
            score += 25
        return score

    ranked = []
    for doc in all_knowledge:
        s = score_chunk(doc)
        if s > 0:
            title = doc.get("title") or doc.get("problem_name") or doc.get("subtopic") or doc.get("document_name") or "Knowledge"
            ranked.append((s, {
                "title": title,
                "topic": doc.get("topic", "General"),
                "subtopic": doc.get("subtopic", ""),
                "difficulty": doc.get("difficulty", "Medium"),
                "pattern": doc.get("subtopic") or doc.get("pattern") or doc.get("topic", "DSA"),
                "tags": doc.get("tags", []),
                "content": doc.get("content", ""),
                "java_code": doc.get("java_code", ""),
                "python_code": doc.get("python_code", ""),
                "hints": doc.get("hints", []),
                "similar": doc.get("similar", []),
                "score": round(float(s) / 100.0, 4),
                "is_relevant": s >= 10,
                "chunk_id": doc.get("chunk_id", ""),
                "source": doc.get("source", "AlgoMentor In-Memory Chunks"),
            }))

    ranked.sort(key=lambda x: x[0], reverse=True)
    selected = [item[1] for item in ranked[:k]]

    if settings.debug_rag:
        print(f"[DEBUG_RAG] In-Memory Fallback retrieved {len(selected)} chunks:")
        for i, r in enumerate(selected, 1):
            print(f"  {i}. [{r['topic']} | {r['title']}] (Score: {r['score']}, Relevant: {r['is_relevant']})")

    return selected


def _build_system_prompt(mode: str = "concept", language: str = "python") -> str:
    lang_name = {
        "python": "Python 3",
        "java": "Java (Modern OOP with java.util)",
        "cpp": "C++ (Modern STL: vector, unordered_map, queue)",
        "javascript": "JavaScript (ES6+)",
    }.get(language.lower(), "Python 3")

    base = (
        "You are AlgoMentor, an elite DSA mentor and algorithmic reasoning engine inspired by ChatGPT.\n"
        "Your mission is to help students and software engineers master Data Structures, Algorithms, "
        "and Technical Coding Interviews with deep understanding.\n\n"
        f"Primary Programming Language for code solutions: {lang_name}.\n\n"
        "Style & Formatting Guidelines:\n"
        "- Format with clean Markdown: use bold headers, clean bullet points, KaTeX/LaTeX for math ($O(N \\log N)$), and syntax-highlighted code blocks.\n"
        "- Structure explanations systematically: Pattern & Mental Intuition -> Step-by-Step Algorithm -> Clean Optimal Code -> Time & Space Complexity -> Edge Cases.\n"
        "- Be encouraging, concise, rigorous, and direct. Never hallucinate complexities.\n\n"
        "Grounding & Topic Relevance Guardrails (CRITICAL):\n"
        "1. You must STRICTLY answer about the specific Data Structure or Algorithm that the user asks about.\n"
        "2. When reference context from the knowledge base is provided, verify that it is relevant to the user's question.\n"
        "3. If any retrieved chunk discusses an UNRELATED topic (for example, context about Stack when the user asked 'Explain trees in DSA'), you MUST COMPLETELY DISREGARD AND REJECT the unrelated context.\n"
        "4. NEVER substitute or confuse different data structures (e.g. NEVER explain Stacks or Queues when asked about Trees).\n"
        "5. If the retrieved context does not contain enough relevant information about the requested topic, explicitly say the knowledge base does not contain enough information and do not hallucinate.\n"
        "6. Use only the retrieved context for the topic being asked; ignore irrelevant chunks completely."
    )

    if mode == "code":
        return base + f"\n\nFocus on providing optimal, production-grade {lang_name} implementations with line-by-line intuition and full Big-O analysis."
    elif mode == "interview":
        return base + "\n\nAct as a senior FAANG Technical Interviewer. Ask clarifying questions, test candidate assumptions on edge cases, evaluate trade-offs, and guide towards the optimal solution."
    elif mode in ("hint", "hint-generation"):
        return base + "\n\nProvide Socratic hints following progressive hint pedagogy. Provide exactly 1 hint tier at a time without giving away the complete solution immediately."
    return base


def _call_external_llm(provider: str, api_key: str, messages: list[dict]) -> Optional[str]:
    """External LLM fallback (Gemini / Groq / OpenAI) if user specifies an API key."""
    try:
        timeout = httpx.Timeout(20.0, connect=2.0)
        if provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
            resp = httpx.post(url, json={"contents": contents}, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        elif provider in ("openai", "groq"):
            endpoint = "https://api.groq.com/openai/v1/chat/completions" if provider == "groq" else "https://api.openai.com/v1/chat/completions"
            model = "llama-3.3-70b-versatile" if provider == "groq" else "gpt-4o-mini"
            resp = httpx.post(
                endpoint,
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": messages},
                timeout=timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return None


def _call_ollama(query: str, context: str, history: list[dict] = None, mode: str = "concept", language: str = "python") -> Optional[str]:
    """Local Ollama call with quick connection timeout to avoid hanging when offline."""
    if not settings.ollama_host:
        return None

    try:
        timeout = httpx.Timeout(12.0, connect=0.8)
        messages = [{"role": "system", "content": _build_system_prompt(mode, language)}]

        if history and isinstance(history, list):
            for h in history[-4:]:
                if isinstance(h, dict) and h.get("role") and h.get("content"):
                    messages.append({"role": h["role"], "content": h["content"]})

        user_content = query
        if context.strip():
            user_content = (
                f"User Question: {query}\n\n"
                f"[Retrieved Reference Context from AlgoMentor DSA Knowledge Base]:\n{context}\n\n"
                f"Instructions: Answer only the requested DSA topic. Use the retrieved context only if it is directly relevant to '{query}'. Ignore unrelated chunks completely. If the retrieved context does not contain enough information for '{query}', explicitly say the knowledge base does not contain enough information for this question and do not hallucinate an answer."
            )

        messages.append({"role": "user", "content": user_content})

        payload = {
            "model": settings.ollama_model,
            "stream": False,
            "messages": messages,
            "options": {
                "temperature": 0.3,
                "num_predict": 400,
            },
        }

        response = httpx.post(f"{settings.ollama_host}/api/chat", json=payload, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            message = data.get("message", {}) if isinstance(data, dict) else {}
            content = message.get("content") if isinstance(message, dict) else None
            if content and content.strip():
                return content.strip()
    except Exception:
        return None
    return None


def _get_code_snippet(doc: dict, language: str) -> tuple[str, str]:
    """Returns (lang_tag, code_snippet) for the requested language."""
    lang = language.lower()
    if lang == "java" and doc.get("java_code"):
        return "java", doc["java_code"]
    elif lang in ("cpp", "c++"):
        return "cpp", doc.get("java_code", doc.get("python_code", ""))
    elif lang in ("javascript", "js"):
        return "javascript", doc.get("python_code", "")
    return "python", doc.get("python_code", doc.get("java_code", ""))


def _generate_progressive_hint(doc: Optional[dict], query: str, requested_level: Optional[int]) -> tuple[str, int]:
    """SRS FR-05: 5-Level Progressive Hint Generation."""
    level = requested_level or 1
    lower = query.lower()
    for num, word in [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]:
        if f"hint {word}" in lower or f"level {word}" in lower:
            level = num
            break

    hints = doc.get("hints", []) if doc else []
    title = doc.get("title", "DSA Problem") if doc else "DSA Problem"

    default_hints = [
        "**Level 1 (General Observation):** Examine the constraints and input ordering. Can you identify an invariant as you iterate through the elements?",
        "**Level 2 (Data Structure Angle):** A brute-force nested loop checks all combinations. Can you use a Hash Map, Two Pointers, or a Monotonic Stack to speed up lookup?",
        "**Level 3 (Core Approach):** Define the mathematical complement or window boundary condition. Express the target condition in terms of known previous states.",
        "**Level 4 (Step-by-step Algorithm):** Maintain two pointers or a running hash table. At each element, check the lookup condition first before inserting the current value.",
        "**Level 5 (Complete Solution):** Review the optimal single-pass algorithm achieving optimal O(N) time and O(1) or O(N) space."
    ]

    hint_text = hints[level - 1] if hints and len(hints) >= level else default_hints[level - 1]

    response = (
        f"### **Progressive Hint — Level {level} of 5 for {title}**\n\n"
        f"{hint_text}\n\n"
        f"--- \n"
        f"*Need more guidance? Click **'Next Hint (Level {min(level + 1, 5)})'** or ask for the complete solution.*"
    )
    return response, level


def _smart_fallback_response(query: str, context: str, docs: list[dict], mode: str, language: str = "python") -> str:
    """Provides an elite algorithmic breakdown when external LLMs are unreachable."""
    lower = query.lower()

    if docs:
        main_doc = docs[0]
        title = main_doc.get("title") or main_doc.get("subtopic") or "DSA Concept"
        content = main_doc.get("content", "")
        pattern = main_doc.get("pattern") or main_doc.get("topic") or "Algorithmic Pattern"
        topic = main_doc.get("topic", "DSA")
        difficulty = main_doc.get("difficulty", "Medium")
        lang_tag, code_body = _get_code_snippet(main_doc, language)

        if not code_body.strip():
            for d in docs + KNOWLEDGE_BASE:
                if d.get("title", "").lower() in title.lower() or title.lower() in d.get("title", "").lower() or d.get("topic", "").lower() == topic.lower():
                    _, alt_code = _get_code_snippet(d, language)
                    if alt_code.strip():
                        code_body = alt_code
                        break

        code_section = ""
        if code_body and code_body.strip():
            code_section = f"#### **2. Optimal Implementation ({lang_tag.capitalize()})**\n```{lang_tag}\n{code_body}\n```\n\n"
        elif mode == "code" or language != "python":
            if lang_tag == "java":
                code_section = f"#### **2. Optimal Implementation (Java)**\n```java\n// Optimal {title} solution in Java\npublic class Solution {{\n    // Traversal and invariant logic\n}}\n```\n\n"
            else:
                code_section = f"#### **2. Optimal Implementation ({lang_tag.capitalize()})**\n```{lang_tag}\n# Optimal {title} solution in {lang_tag.capitalize()}\n```\n\n"

        response = (
            f"### **{title}**\n\n"
            f"**Topic:** `{topic}` | **Pattern:** `{pattern}` | **Difficulty:** `{difficulty}`\n\n"
            f"#### **1. Intuition & Mental Model**\n"
            f"{content}\n\n"
            f"{code_section}"
            f"#### **3. Complexity Analysis**\n"
            f"- **Time Complexity:** $O(N)$ or $O(\\log N)$ depending on traversal steps.\n"
            f"- **Space Complexity:** $O(1)$ auxiliary space for pointers or $O(N)$ for auxiliary storage.\n\n"
            f"#### **4. Edge Cases & Interview Traps**\n"
            f"- Empty collections or single-element inputs.\n"
            f"- Duplicate elements and boundary conditions.\n"
            f"- Integer overflow when computing midpoints (use `l + (r - l) / 2`).\n\n"
            f"*(Retrieved context from AlgoMentor DSA Knowledge Base)*"
        )
        return response

    if "tree" in lower:
        return (
            "### **Trees & Binary Trees in DSA**\n\n"
            "**1. Core Intuition:**\n"
            "A tree is a non-linear, hierarchical data structure composed of nodes connected by directed or undirected edges, containing no cycles. Each tree has a single root node, and every non-root node has exactly one parent.\n\n"
            "**2. Traversal Techniques:**\n"
            "- **Depth-First Search (DFS):** Inorder (Left, Root, Right), Preorder (Root, Left, Right), Postorder (Left, Right, Root).\n"
            "- **Breadth-First Search (BFS):** Level-Order Traversal using a FIFO queue.\n\n"
            "**3. Complexity Analysis:**\n"
            "- **Balanced BST Search/Insert:** $O(\\log N)$ time, $O(H)$ stack space.\n"
            "- **Skewed BST Search/Insert:** $O(N)$ worst-case time.\n\n"
            "*(Retrieved context from AlgoMentor DSA Knowledge Base)*"
        )

    if "binary search" in lower:
        return (
            "### **Binary Search Algorithm**\n\n"
            "**1. Core Intuition:**\n"
            "Binary search repeatedly evaluates the middle element of a sorted collection, halving the remaining candidates.\n\n"
            "**2. Complexity Analysis:**\n"
            "- **Time Complexity:** $O(\\log N)$ guaranteed.\n"
            "- **Space Complexity:** $O(1)$ iterative auxiliary space.\n\n"
            "```python\ndef binary_search(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: left = mid + 1\n        else: right = mid - 1\n    return -1\n```\n\n"
            "*(Retrieved context from AlgoMentor DSA Knowledge Base)*"
        )

    return (
        f"### **AlgoMentor Breakdown for '{query}'**\n\n"
        f"**1. Recommended Algorithmic Pattern:**\n"
        f"Analyze constraints: If $N \\le 10^5$, aim for an $O(N)$ or $O(N \\log N)$ optimal pattern (Two Pointers, Sliding Window, or Hash Map).\n\n"
        f"**2. Complexity Analysis:**\n"
        f"- **Time Complexity:** $O(N)$ single-pass optimal target.\n"
        f"- **Space Complexity:** $O(1)$ auxiliary pointer space.\n\n"
        f"Ask me for progressive hints, edge case analysis, or complete code in Python/Java/C++!"
    )


def build_agent_workflow():
    def rewrite_node(state):
        original = state["message"]
        history = state.get("history", [])
        state["rewritten_query"] = rewrite_query(original, history)
        return state

    def route_node(state):
        query = state.get("rewritten_query", state["message"])
        route = route_query(query, state.get("mode", "concept"))
        state["route"] = route
        return state

    def retrieve_node(state):
        query = state.get("rewritten_query", state["message"])
        docs = retrieve_context(query)
        state["docs"] = docs
        state["context"] = "\n\n".join(f"[{doc.get('topic', 'DSA')} - {doc.get('title', 'Concept')}]:\n{doc.get('content', '')}" for doc in docs)
        return state

    def response_node(state):
        route = state["route"]
        message = state["message"]
        rewritten = state.get("rewritten_query", message)
        context = state.get("context", "")
        docs = state.get("docs", [])
        history = state.get("history", [])
        api_key = state.get("api_key")
        provider = state.get("provider")
        language = state.get("language", "python")
        user_email = state.get("user_email") or "demo@example.com"
        hint_level = state.get("hint_level")

        primary_doc = docs[0] if docs else None
        pattern = primary_doc.get("pattern") if primary_doc else None
        similar = primary_doc.get("similar", []) if primary_doc else []

        state["pattern"] = pattern
        state["similar_problems"] = similar
        state["suggested_next_actions"] = []

        # 1. Beginner Roadmap
        if route == "beginner-roadmap":
            state["answer"] = (
                "Here is a practical DSA roadmap for a BTech beginner to start your journey:\n\n"
                "1. Start with arrays and strings: learn indexing, traversal, prefix sums, two pointers, and sliding window.\n"
                "2. Master core linear data structures: arrays, hash maps, linked lists (fast/slow pointers), stacks, and queues.\n"
                "3. Move to searching and sorting: linear search, binary search (exact value and answer space), merge sort, and quick sort.\n"
                "4. Build consistent problem-solving habits: solve 2-3 problems daily and analyze time and space complexity.\n"
                "5. Learn recursion and backtracking before moving to dynamic programming.\n"
                "6. Study hierarchical structures: binary trees, binary search trees, and heaps/priority queues.\n"
                "7. Master graphs and dynamic programming: BFS, DFS, Topological Sort (Kahn's), and 1D/2D DP.\n"
                "8. Follow curated roadmaps like Striver's A-to-Z DSA sheet for structured interview readiness.\n\n"
                "Recommended progression: Arrays -> Strings -> Hashing -> Binary Search -> Stacks/Queues -> Trees -> Graphs -> DP."
            )
            state["suggested_next_actions"] = ["Explain Arrays & Two Pointers", "Start with Binary Search", "What is Big-O?"]

        # 2. Practice Plan (FR-17)
        elif route == "practice-plan":
            plan = build_practice_plan(user_email, number_of_problems=4)
            state["answer"] = (
                f"### **Targeted Practice Plan for `{user_email}`**\n\n"
                f"- **Focus Topics:** {plan['focus_topics']}\n"
                f"- **Target Difficulty:** {plan.get('target_difficulty', 'Medium')}\n"
                f"- **Curated Problems:**\n"
                f"  1. **Two Sum** (Hash Map complement pattern)\n"
                f"  2. **Binary Search** (Divide and conquer search space)\n"
                f"  3. **Maximum Subarray** (Kadane's running sum)\n"
                f"  4. **Course Schedule** (Topological Sort / Kahn's algorithm)\n\n"
                f"This targeted sequence reinforces pattern recognition and interview readiness."
            )
            state["suggested_next_actions"] = ["Solve Two Sum", "Explain Kadane's Algorithm", "Show Course Schedule"]

        # 3. Progress Analysis (FR-15, FR-16)
        elif route == "progress-analysis":
            summary = get_progress_summary(user_email)
            solved = summary.get("solved_count", 0)
            attempted = summary.get("attempted_count", 0)
            weak = summary.get("weak_topics", [])
            state["answer"] = (
                f"### **DSA Progress & Weak Area Analysis**\n\n"
                f"- **Account:** `{user_email}`\n"
                f"- **Solved Problems:** **{solved}**\n"
                f"- **Attempted Problems:** **{attempted}**\n"
                f"- **Identified Growth Topics:** {', '.join(weak) if weak else 'Dynamic Programming, Graph Traversal, Binary Search'}\n\n"
                f"**Recommendation:** Focus your next session on strengthening pattern recognition in your growth topics!"
            )
            state["suggested_next_actions"] = ["Create a DP Practice Plan", "Explain Sliding Window Pattern", "Simulate Mock Interview"]

        # 4. Progressive Hints (FR-05)
        elif route == "hint-generation":
            hint_resp, resolved_level = _generate_progressive_hint(primary_doc, rewritten, hint_level)
            state["answer"] = hint_resp
            state["hint_level"] = resolved_level
            next_lvl = min(resolved_level + 1, 5)
            state["suggested_next_actions"] = [
                f"Give Hint {next_lvl}",
                "Explain Time Complexity",
                f"Show {language.capitalize()} Solution"
            ]

        # 5. Similar Problem Recommendations (FR-06)
        elif route == "similar-problems":
            rec_text = "### **Similar Problems & Pattern Connections**\n\n"
            if similar:
                for item in similar:
                    rec_text += f"- **{item['title']}** (`{item.get('difficulty', 'Medium')}`) — *Pattern:* `{item.get('pattern', 'Similar Pattern')}`\n"
            else:
                rec_text += (
                    "- **Two Sum** (Easy) — *Pattern:* Hash Map Complement\n"
                    "- **3Sum** (Medium) — *Pattern:* Sorting + Two Pointers\n"
                    "- **Container With Most Water** (Medium) — *Pattern:* Two Pointers\n"
                )
            rec_text += "\nThese problems share identical invariant checking and traversal paradigms."
            state["answer"] = rec_text
            state["suggested_next_actions"] = ["Explain the first problem", "Show solution approach"]

        # 6. General / Problem / Concept RAG Synthesis
        else:
            answer = None

            if api_key and provider:
                sys_prompt = _build_system_prompt(route, language)
                ext_messages = [{"role": "system", "content": sys_prompt}]
                if history:
                    ext_messages.extend(history[-4:])
                user_msg = f"{rewritten}\n\nContext from DSA Knowledge Base:\n{context}" if context else rewritten
                ext_messages.append({"role": "user", "content": user_msg})
                answer = _call_external_llm(provider, api_key, ext_messages)

            if settings.debug_rag:
                print(f"[DEBUG_RAG] User Query: {rewritten}")
                print(f"[DEBUG_RAG] Query Embedding Model: {settings.embedding_model}")
                print(f"[DEBUG_RAG] Final context sent to Llama:\n{context}\n")

            if not answer:
                answer = _call_ollama(rewritten, context, history=history, mode=route, language=language)

            if not answer:
                answer = _smart_fallback_response(rewritten, context, docs, route, language=language)

            if "complexity" in message.lower() and "complexity" not in answer.lower():
                answer += "\n\n**Complexity Analysis:**\n- **Time Complexity:** $O(N)$ for single-pass traversal.\n- **Space Complexity:** $O(1)$ auxiliary pointer storage."

            if docs and "retrieved" not in answer.lower():
                answer += f"\n\n*(Retrieved context from AlgoMentor DSA Knowledge Base)*"

            state["answer"] = answer
            state["suggested_next_actions"] = [
                "Explain Time & Space Complexity",
                "Give a Progressive Hint",
                f"Show in {'Java' if language == 'python' else 'Python'}",
                "Recommend Similar Problems"
            ]

        return state

    workflow = StateGraph(dict)
    workflow.add_node("rewrite", rewrite_node)
    workflow.add_node("route", route_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("response", response_node)

    workflow.set_entry_point("rewrite")
    workflow.add_edge("rewrite", "route")
    workflow.add_edge("route", "retrieve")
    workflow.add_edge("retrieve", "response")
    workflow.add_edge("response", END)
    return workflow.compile()


def generate_response(chat: ChatMessage) -> ChatResponse:
    workflow = build_agent_workflow()
    state = workflow.invoke({
        "message": chat.message,
        "mode": chat.mode,
        "history": chat.history,
        "api_key": chat.api_key,
        "provider": chat.provider,
        "language": getattr(chat, "language", "python") or "python",
        "user_email": getattr(chat, "user_email", None),
        "hint_level": getattr(chat, "hint_level", None),
    })
    docs = state.get("docs", [])
    return ChatResponse(
        response=state.get("answer", ""),
        mode=state.get("route", route_query(chat.message, chat.mode)),
        sources=[doc["title"] for doc in docs],
        pattern=state.get("pattern"),
        hint_level=state.get("hint_level"),
        suggested_next_actions=state.get("suggested_next_actions", []),
        similar_problems=state.get("similar_problems", []),
    )
