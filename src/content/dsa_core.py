"""Data Structures & Algorithms subtopics (bonus topic)."""

SUBTOPICS = [
    dict(
        id="big-o-notation",
        title="Big-O Notation: Measuring Cost, Not Speed",
        hook="Big-O doesn't measure how fast code runs — it measures how the amount of work grows as the input grows, which is a far more durable thing to reason about.",
        explanation=(
            "Big-O notation describes the upper bound on how an algorithm's running time (or memory use) grows "
            "as the input size `n` grows, ignoring constant factors and lower-order terms. `O(n)` means work "
            "grows linearly with input size; `O(n^2)` means work grows with the square of it — a nested loop "
            "over the same list is the classic example. `O(log n)` describes algorithms like binary search that "
            "cut the problem in half at each step, so doubling the input barely increases the work.\n\n"
            "The value of Big-O is comparative and asymptotic: an `O(n)` algorithm will always eventually "
            "outperform an `O(n^2)` one as `n` grows large enough, regardless of implementation details, which "
            "is why it's the right tool for reasoning about how code will behave at scale, not for predicting "
            "exact runtime on a specific machine."
        ),
        code=dict(
            lang="python",
            label="Same task, two very different growth rates",
            src=(
                "# O(n^2): nested loop checks every pair\n"
                "def has_duplicate_slow(nums):\n"
                "    for i in range(len(nums)):\n"
                "        for j in range(i + 1, len(nums)):\n"
                "            if nums[i] == nums[j]:\n"
                "                return True\n"
                "    return False\n\n"
                "# O(n): a single pass using a set for O(1) lookups\n"
                "def has_duplicate_fast(nums):\n"
                "    seen = set()\n"
                "    for num in nums:\n"
                "        if num in seen:\n"
                "            return True\n"
                "        seen.add(num)\n"
                "    return False"
            ),
        ),
        example=(
            "On a list of 1,000 items the O(n^2) duplicate check runs roughly a million comparisons, while the "
            "O(n) version runs about a thousand — the gap that looks academic at small sizes becomes the "
            "difference between milliseconds and minutes once `n` reaches a few million rows, exactly the kind "
            "of scale a production system eventually hits."
        ),
        best_practices=[
            "Identify nested loops over the same data early — they're the most common source of accidental O(n^2) behavior.",
            "Reach for a set or dict for membership checks (`x in collection`) instead of a list whenever that check happens repeatedly — O(1) versus O(n) per lookup.",
            "Profile before optimizing on real data; Big-O tells you how something scales, not whether it's currently your actual bottleneck.",
        ],
        pitfalls=[
            "Using `x in my_list` inside a loop, silently turning an otherwise linear algorithm into a quadratic one.",
            "Confusing Big-O with actual wall-clock speed — a well-implemented O(n^2) algorithm can outperform a poorly implemented O(n log n) one for small, realistic input sizes.",
        ],
        prompts=[
            "What's the time complexity of this function, and how would you improve it?",
            "Explain the difference between O(n log n) and O(n^2) with a concrete input size example.",
            "When does an algorithm's Big-O complexity actually matter in a real application?",
        ],
    ),
    dict(
        id="arrays-linked-lists",
        title="Arrays vs. Linked Lists",
        hook="These two structures store the same kind of data — a sequence of items — but make opposite trade-offs on nearly every operation.",
        explanation=(
            "An array (Python's `list`) stores elements in contiguous memory, which makes indexing (`arr[i]`) an "
            "O(1) operation — the computer can jump directly to the right memory address by doing simple "
            "arithmetic. Inserting or removing an element in the middle is O(n), though, because every following "
            "element has to shift over to keep the array contiguous.\n\n"
            "A linked list stores each element in its own node, holding a value and a pointer to the next node, "
            "scattered anywhere in memory. Inserting or removing a node once you already have a reference to its "
            "position is O(1) — you just rewire a couple of pointers — but there's no way to jump directly to "
            "the 5th element; you have to walk the list from the start, making indexed access O(n)."
        ),
        code=dict(
            lang="python",
            label="A minimal singly linked list",
            src=(
                "class Node:\n"
                "    def __init__(self, value):\n"
                "        self.value = value\n"
                "        self.next = None\n\n"
                "class LinkedList:\n"
                "    def __init__(self):\n"
                "        self.head = None\n\n"
                "    def prepend(self, value):          # O(1)\n"
                "        node = Node(value)\n"
                "        node.next = self.head\n"
                "        self.head = node\n\n"
                "    def find(self, value):              # O(n) — no direct indexing\n"
                "        current = self.head\n"
                "        while current:\n"
                "            if current.value == value:\n"
                "                return True\n"
                "            current = current.next\n"
                "        return False"
            ),
        ),
        example=(
            "A music player's 'undo last skip' history is naturally a linked structure — constantly adding to "
            "the front is cheap — while the playlist itself, which the UI needs to jump around in by index "
            "('play track 12'), is much better served by an array-backed structure like Python's `list`."
        ),
        best_practices=[
            "Default to Python's built-in `list` for almost everything — it's array-backed, highly optimized, and the right choice unless you have a specific reason not to use it.",
            "Reach for a linked-list-style structure (or `collections.deque` for a doubly-linked-list-like queue) specifically when you need fast insertion/removal at the ends without shifting elements.",
            "Use `collections.deque` instead of a plain list when you need O(1) appends and pops from both ends, such as implementing a queue.",
        ],
        pitfalls=[
            "Inserting at the front of a Python list (`list.insert(0, x)`) repeatedly, which is O(n) per call and quietly quadratic across a loop.",
            "Reaching for a hand-rolled linked list in Python for general-purpose use when a built-in list or deque already covers the need with far less code.",
        ],
        prompts=[
            "Why is inserting at the start of a Python list slow, and what should I use instead?",
            "When would a linked list actually outperform an array in practice?",
            "Implement a doubly linked list with insert and delete operations.",
        ],
    ),
    dict(
        id="hash-tables",
        title="Hash Tables: Why Dicts Are (Usually) O(1)",
        hook="A Python dict looking up a key in roughly constant time regardless of how many items it holds isn't magic — it's a hash function doing very deliberate work.",
        explanation=(
            "A hash table stores key-value pairs by running each key through a hash function that converts it "
            "into an integer, then uses that integer (modulo the table's size) to decide which 'bucket' to store "
            "the pair in. Looking up a key means hashing it the same way and going straight to that bucket, "
            "which is why well-designed hash table operations average O(1) regardless of how many items are stored.\n\n"
            "Two different keys can hash to the same bucket — a collision — and how a hash table handles that "
            "(chaining, where each bucket holds a small list; or open addressing, where it probes for the next "
            "free slot) affects worst-case performance. In practice, Python's `dict` and `set` handle this "
            "automatically and efficiently, resizing the underlying table as it grows to keep collisions rare."
        ),
        code=dict(
            lang="python",
            label="Word frequency count — the canonical hash table use case",
            src=(
                "from collections import defaultdict\n\n"
                "def word_frequencies(text):\n"
                "    counts = defaultdict(int)     # dict under the hood\n"
                "    for word in text.lower().split():\n"
                "        counts[word] += 1          # O(1) average lookup + update\n"
                "    return dict(counts)\n\n"
                "word_frequencies(\"the cat sat on the mat the cat liked\")\n"
                "# {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1, 'liked': 1}"
            ),
        ),
        example=(
            "Caching expensive function results in a dict keyed by the function's arguments turns a repeated, "
            "slow computation into a near-instant lookup after the first call — the same principle behind "
            "`functools.lru_cache`, which is a hash table wearing a decorator."
        ),
        best_practices=[
            "Only use immutable, hashable types (strings, numbers, tuples of hashable items) as dict keys — Python enforces this because mutable keys would break the hash-to-bucket mapping if they changed after insertion.",
            "Reach for a set when you only care about membership ('have I seen this before?') rather than a full dict when you don't actually need an associated value.",
            "Use `dict.get(key, default)` or `defaultdict` instead of checking `if key in dict` followed by a separate lookup — it avoids doing the hash lookup twice.",
        ],
        pitfalls=[
            "Trying to use a list or another dict as a dictionary key, hitting a `TypeError: unhashable type`.",
            "Assuming dict lookups are always O(1) in the absolute worst case — a poor hash function with many collisions can degrade toward O(n), though Python's implementation makes this rare in practice.",
        ],
        prompts=[
            "Why can't I use a list as a dictionary key in Python?",
            "Explain how hash collisions are handled and why they matter for performance.",
            "Rewrite this nested-loop lookup to use a dict for O(1) access instead.",
        ],
    ),
    dict(
        id="stacks-queues",
        title="Stacks & Queues",
        hook="Same basic idea — a line of items — but opposite rules for what comes out next, and that one rule difference is what makes each useful for very different problems.",
        explanation=(
            "A stack follows Last-In-First-Out (LIFO): the most recently added item is the first one removed, "
            "like a stack of plates. It's the structure behind function call tracking (the 'call stack'), "
            "undo/redo features, and depth-first search. A queue follows First-In-First-Out (FIFO): the first "
            "item added is the first one removed, like a line at a checkout counter. It's the structure behind "
            "task scheduling, breadth-first search, and print job processing.\n\n"
            "In Python, a plain `list` works fine as a stack (`append`/`pop` from the end, both O(1)), but makes "
            "a poor queue, because removing from the front (`pop(0)`) is O(n) — it has to shift every remaining "
            "element. `collections.deque` supports O(1) operations at both ends, making it the right tool for a queue."
        ),
        code=dict(
            lang="python",
            label="Stack with list, queue with deque",
            src=(
                "# Stack (LIFO) — plain list is fine\n"
                "stack = []\n"
                "stack.append(\"a\")\n"
                "stack.append(\"b\")\n"
                "stack.pop()                # 'b' — last in, first out\n\n"
                "# Queue (FIFO) — use deque, not list\n"
                "from collections import deque\n"
                "queue = deque()\n"
                "queue.append(\"a\")\n"
                "queue.append(\"b\")\n"
                "queue.popleft()             # 'a' — first in, first out, O(1)"
            ),
        ),
        example=(
            "A browser's 'back button' history is a stack — the most recently visited page is the first one you "
            "return to — while a customer support ticketing system processing requests in the order they arrived "
            "is a queue, since fairness demands first-come, first-served."
        ),
        best_practices=[
            "Use `collections.deque` for any queue in Python — `list.pop(0)` is a common, easy-to-miss O(n) performance trap.",
            "Reach for a stack (recursion, or an explicit list used as one) when a problem is naturally 'handle the most recent thing first,' like matching parentheses or undo history.",
            "Reach for a queue when a problem is naturally 'handle things in the order they arrived,' like breadth-first traversal or task processing.",
        ],
        pitfalls=[
            "Using a plain Python list as a queue with repeated `pop(0)` calls, silently making an otherwise-linear algorithm quadratic.",
            "Confusing which structure a problem needs — using a stack (LIFO) where fairness or arrival order actually matters (FIFO), or vice versa.",
        ],
        prompts=[
            "Why is deque preferred over list for a queue in Python?",
            "Write a function that checks whether parentheses in a string are balanced, using a stack.",
            "Explain how a stack underlies function recursion and the call stack.",
        ],
    ),
]
