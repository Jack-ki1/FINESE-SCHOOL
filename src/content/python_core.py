"""
Python — core language subtopics.

Schema per lesson (kept consistent across every topic file in this
package so templates/app.js never need topic-specific logic):

  id, title, hook, explanation, deep_dive, code, advanced_code,
  example, best_practices, pitfalls, glossary, faq, quiz, prompts
"""

SUBTOPICS = [
    dict(
        id="variables-datatypes",
        title="Variables & Data Types",
        hook="Python variables aren't boxes that hold values — they're labels pointing at objects, and that one distinction explains half of the 'weird' behavior beginners run into.",
        explanation=(
            "In many languages, a variable is a named slot of memory that holds a value directly. Python works "
            "differently: every value is an object living somewhere in memory, and a variable is just a name "
            "bound to that object. Writing `x = 5` doesn't put `5` inside a box called `x` — it creates the "
            "integer object `5` (or reuses an existing one) and points the name `x` at it. Writing `y = x` "
            "doesn't copy the value into a new box either; it points `y` at the exact same object `x` is "
            "already pointing at.\n\n"
            "Python's built-in types split into two camps based on whether their objects can change after "
            "creation. Immutable types — `int`, `float`, `str`, `tuple`, `bool`, `frozenset` — can never be "
            "modified in place; any operation that looks like a modification actually creates a brand new "
            "object and rebinds the name to it. Mutable types — `list`, `dict`, `set`, and custom classes by "
            "default — can be changed in place, meaning every name pointing at that object sees the change.\n\n"
            "This distinction is why `a = [1, 2, 3]; b = a; b.append(4)` leaves `a` also showing `[1, 2, 3, 4]` "
            "— `b` was never a copy, just another label on the same list object. The same operation with an "
            "immutable type behaves completely differently: `a = 5; b = a; b += 1` leaves `a` as `5`, because "
            "`b += 1` created a new integer object `6` and rebound only `b` to it.\n\n"
            "Python is also dynamically typed: a variable name can be rebound to an object of a completely "
            "different type at any time (`x = 5; x = \"now a string\"` is perfectly legal), and type checking "
            "happens at runtime, not compile time. This gives flexibility but shifts the burden of catching "
            "type mistakes onto testing and, optionally, static type checkers reading your type hints."
        ),
        deep_dive=(
            "CPython (the reference implementation almost everyone runs) optimizes small integers and short "
            "strings by caching and reusing them — the integers -5 through 256 are pre-allocated singletons, "
            "so `a = 200; b = 200; a is b` is `True`, while `a = 500; b = 500; a is b` is often `False` even "
            "though `a == b` is still `True`. This is a CPython implementation detail, not a language "
            "guarantee, and it's exactly why you should compare values with `==` and reserve `is` for checking "
            "identity against singletons like `None`.\n\n"
            "Every object carries a reference count — the number of names and containers currently pointing at "
            "it. When that count drops to zero, CPython's garbage collector reclaims the memory immediately "
            "(with a separate cyclic collector handling reference cycles that pure reference counting can't "
            "resolve on its own, like two objects that point at each other). `sys.getrefcount(obj)` shows this "
            "count directly, and it's a useful way to understand exactly when Python considers an object "
            "eligible for cleanup.\n\n"
            "Type annotations (`x: int = 5`) don't change any of this runtime behavior at all — Python never "
            "enforces them while the program runs. They exist purely for readability and for external tools "
            "like `mypy` to catch mismatches before the code ever executes, which is why a type-checked "
            "codebase still needs `assert` or explicit validation for anything that actually must be correct "
            "at runtime, such as data coming from a user or an API."
        ),
        code=dict(
            lang="python",
            label="Variables as labels, not boxes",
            src=(
                "a = [1, 2, 3]\n"
                "b = a                # b points at the SAME list object\n"
                "b.append(4)\n"
                "print(a)             # [1, 2, 3, 4] -- a changed too\n\n"
                "x = 5\n"
                "y = x                # y points at the same int object (for now)\n"
                "y += 1               # creates a NEW int object, rebinds y only\n"
                "print(x, y)          # 5 6 -- x is untouched"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Identity vs. equality, and the small-int cache",
            src=(
                "a = 200\n"
                "b = 200\n"
                "print(a is b)        # True -- CPython caches small ints (-5 to 256)\n\n"
                "c = 500\n"
                "d = 500\n"
                "print(c is d)        # Often False -- not cached, separate objects\n"
                "print(c == d)        # True -- value equality still holds\n\n"
                "# The correct rule: use == for value comparisons, always.\n"
                "# Reserve `is` for singletons: None, True, False.\n"
                "value = None\n"
                "if value is None:    # idiomatic\n"
                "    print(\"empty\")"
            ),
        ),
        example=(
            "A function that receives a list argument and calls `.sort()` on it inside the function will "
            "silently sort the caller's original list too — a common source of 'spooky action at a distance' "
            "bugs that only makes sense once you internalize that the function received a reference to the "
            "same object, not a private copy."
        ),
        best_practices=[
            "Use `==` to compare values and reserve `is` strictly for identity checks against `None`, `True`, and `False`.",
            "Never use a mutable default argument (`def f(items=[])`) — the same list object is reused across every call, silently accumulating state.",
            "Explicitly copy a list or dict (`list(original)`, `dict.copy()`, or `copy.deepcopy()` for nested structures) whenever you need an independent version.",
            "Add type hints to function signatures even though Python won't enforce them — they document intent and let tools like mypy catch mistakes early.",
            "Prefer descriptive variable names over single letters outside of very short loops or well-known math contexts.",
            "Remember that `+=` on an immutable type creates a new object; on a mutable type (like a list) it usually mutates in place — know which one you're touching.",
        ],
        pitfalls=[
            "Defining `def add_item(item, items=[]):` and being surprised that `items` keeps growing across unrelated calls — the default list is created once, at function definition time, and reused forever.",
            "Assuming `b = a` creates a copy of a list or dict, then being confused when modifying `b` also changes `a`.",
            "Using `is` to compare numbers or strings for equality, which works by coincidence on small cached values and then mysteriously breaks on larger ones.",
            "Forgetting that `str`, `tuple`, and `frozenset` are immutable, and trying to modify them in place (`my_tuple[0] = 5`) instead of building a new one.",
        ],
        glossary=[
            dict(term="Mutable", definition="An object whose internal state can change after creation without changing its identity (its memory address) — lists, dicts, sets."),
            dict(term="Immutable", definition="An object that can never be changed after creation — any 'modification' actually produces a new object. Applies to int, float, str, tuple, bool, frozenset."),
            dict(term="Reference / binding", definition="The relationship between a variable name and the object it points to. Assignment creates or changes a binding; it does not copy the object."),
            dict(term="Identity", definition="Whether two names point at the literal same object in memory, checked with `is` and returned by `id()`."),
            dict(term="Dynamic typing", definition="A variable's type is determined by whatever object it currently points to, and can change across the variable's lifetime — Python checks types at runtime, not compile time."),
        ],
        faq=[
            dict(q="If Python has no true 'variables that hold values', how does `x = x + 1` work?", a="It evaluates the right side first (look up what x points to, add 1, producing a brand-new int object), then rebinds the name x to that new object. The old object x used to point to is unaffected and gets garbage collected if nothing else references it."),
            dict(q="Why does `a = [1,2]; b = [1,2]; print(a == b)` print True but `print(a is b)` print False?", a="== compares values (both lists contain the same elements, so True). is compares identity (they're two separate list objects that happen to look the same, so False)."),
            dict(q="Is Python 'pass by reference' or 'pass by value'?", a="Neither term fits cleanly — the common description is 'pass by object reference' (or 'pass by assignment'): the function parameter is a new name bound to the same object the caller passed. You can mutate that object through the parameter, but rebinding the parameter to a new object doesn't affect the caller's variable."),
        ],
        quiz=[
            dict(
                question="What does the following print?\na = [1, 2]\nb = a\na.append(3)\nprint(b)",
                options=["[1, 2]", "[1, 2, 3]", "Error", "[3]"],
                correct=1,
                explanation="b points at the same list object as a, so appending through a is visible through b too.",
            ),
            dict(
                question="Which of these types is mutable?",
                options=["tuple", "str", "list", "int"],
                correct=2,
                explanation="Lists can be changed in place (append, remove, sort); the other three are immutable in Python.",
            ),
            dict(
                question="Why is `def f(items=[]):` considered a bug-prone pattern?",
                options=[
                    "Lists can't be function arguments",
                    "The default list is created once and shared across all calls that don't pass their own list",
                    "It causes a syntax error",
                    "Python requires default arguments to be immutable",
                ],
                correct=1,
                explanation="Default argument values are evaluated once, at function definition time, not on every call — so a mutable default silently accumulates state across calls.",
            ),
        ],
        prompts=[
            "Explain why my function is modifying a list I didn't mean to change.",
            "What's the difference between == and is in Python, with examples?",
            "Why is a mutable default argument considered a bug, and how do I fix it?",
            "Walk through what happens in memory when I write b = a for a list.",
            "When would I actually want to use `is` instead of `==`?",
            "Show me how copy.deepcopy differs from a shallow copy for nested lists.",
        ],
    ),
    dict(
        id="control-flow",
        title="Control Flow: Conditionals & Loops",
        hook="Python's control flow looks simple on the surface, but the for-else and while-else clauses trip up even experienced developers coming from other languages because no other mainstream language has them.",
        explanation=(
            "`if` / `elif` / `else` in Python works largely as you'd expect from any language, with one notable "
            "difference: there's no switch/case statement in versions before 3.10 (Python 3.10 introduced "
            "`match`/`case` as a structural pattern matching statement, not a direct switch equivalent). Python "
            "also has no braces — indentation itself defines blocks, which means consistent whitespace isn't a "
            "style preference, it's part of the syntax.\n\n"
            "`for` loops iterate over any iterable (not just numeric ranges) — a list, a string, a dict's keys, "
            "a file object's lines, or any custom object implementing the iterator protocol. `range(n)` "
            "generates numbers lazily rather than building a list up front, which is why looping over "
            "`range(10_000_000)` doesn't consume 10 million integers' worth of memory. `while` loops run as "
            "long as a condition holds, useful when the number of iterations isn't known ahead of time.\n\n"
            "Both `for` and `while` loops support an unusual `else` clause that runs only if the loop completed "
            "without hitting a `break`. This is genuinely useful for search-and-fallback patterns: loop through "
            "items looking for something, and if you never `break` out (meaning you never found it), the "
            "`else` block runs your 'not found' logic — no flag variable required.\n\n"
            "`break` exits the nearest enclosing loop entirely; `continue` skips the rest of the current "
            "iteration and moves to the next one. Python has no `goto` and no labeled break (no way to break "
            "out of two nested loops at once directly) — the idiomatic workaround is extracting the nested "
            "loops into a function and using `return`, or using a flag variable, or raising and catching a "
            "custom exception for genuinely tangled cases."
        ),
        deep_dive=(
            "The `match` statement (3.10+) is structural pattern matching, considerably more powerful than a "
            "C-style switch. It can destructure data while matching: `match point: case (0, 0): ... case (x, "
            "0): ...` binds `x` automatically when the second element is zero. It can match against class "
            "instances by their attributes, match against literal values, and use guard clauses (`case (x, y) "
            "if x == y:`). This makes it genuinely useful for parsing structured data (like a JSON-derived "
            "dict or an AST), not just a cosmetic alternative to chained `elif`.\n\n"
            "Truthiness matters constantly in Python conditionals: `if some_list:` checks for emptiness "
            "(`[]` is falsy, any non-empty list is truthy), `if some_string:` checks for an empty string, and "
            "`if some_dict:` checks for an empty dict — you rarely need `if len(x) > 0:` or `if x != \"\":` "
            "explicitly. This is idiomatic Python but occasionally surprising for values like `0`, `0.0`, and "
            "`None`, which are all falsy despite being 'real' values in many contexts.\n\n"
            "Chained comparisons (`if 0 < x < 10:`) evaluate the way they read mathematically, unlike languages "
            "where `0 < x < 10` would silently evaluate left-to-right as `(0 < x) < 10` (comparing a boolean to "
            "10). Python treats the chain as `0 < x and x < 10`, evaluating `x` only once."
        ),
        code=dict(
            lang="python",
            label="for-else for a clean search pattern",
            src=(
                "def find_first_negative(numbers):\n"
                "    for n in numbers:\n"
                "        if n < 0:\n"
                "            print(f\"Found: {n}\")\n"
                "            break\n"
                "    else:\n"
                "        print(\"No negative numbers found\")\n\n"
                "find_first_negative([4, 7, -2, 9])   # Found: -2\n"
                "find_first_negative([4, 7, 2, 9])    # No negative numbers found"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Structural pattern matching with match/case (3.10+)",
            src=(
                "def handle_response(response):\n"
                "    match response:\n"
                "        case {\"status\": 200, \"data\": data}:\n"
                "            return f\"Success: {data}\"\n"
                "        case {\"status\": 404}:\n"
                "            return \"Not found\"\n"
                "        case {\"status\": code} if code >= 500:\n"
                "            return f\"Server error: {code}\"\n"
                "        case _:\n"
                "            return \"Unknown response shape\"\n\n"
                "handle_response({\"status\": 200, \"data\": [1, 2, 3]})   # 'Success: [1, 2, 3]'"
            ),
        ),
        example=(
            "A CLI tool parsing a subcommand ('init', 'build', 'deploy') reads far more clearly as a `match` "
            "statement against the command string than as a chain of five `elif` branches, especially once each "
            "branch also needs to destructure different sets of trailing arguments."
        ),
        best_practices=[
            "Rely on truthiness (`if items:`) instead of explicit length or emptiness checks for lists, strings, and dicts.",
            "Use `for...else` for search-with-fallback logic instead of a manual 'found' boolean flag.",
            "Reach for `match`/`case` when you're matching against several possible *shapes* of data, not just several possible values of one variable — for a simple value switch, `if/elif` is often just as clear.",
            "Extract deeply nested loops into a helper function and use `return` to exit early, rather than juggling multiple break flags.",
            "Use chained comparisons (`0 <= x < 10`) instead of `x >= 0 and x < 10` — it's shorter and mirrors mathematical notation.",
        ],
        pitfalls=[
            "Confusing `for...else` to mean 'else if the loop ran' — it actually means 'else if the loop was NOT broken out of', which is the opposite of what the keyword suggests to most newcomers.",
            "Trying to `break` out of two nested loops with a single `break` statement — it only exits the innermost loop.",
            "Mixing tabs and spaces for indentation, which can look identical in some editors but causes a `TabError` or silently different block structure.",
            "Forgetting that `0`, `0.0`, `\"\"`, `[]`, `{}`, and `None` are all falsy, leading to unexpected branches when a valid-but-empty value flows into a conditional.",
        ],
        glossary=[
            dict(term="Truthiness", definition="Whether a non-boolean value counts as True or False in a boolean context; empty collections, 0, 0.0, and None are falsy, virtually everything else is truthy."),
            dict(term="Iterable", definition="Any object you can loop over with a for loop — lists, strings, dicts, files, generators, and anything implementing __iter__."),
            dict(term="Structural pattern matching", definition="The match/case statement's ability to match not just values but the shape of data (e.g. a dict with certain keys, a tuple of a certain length)."),
            dict(term="Guard clause (in match)", definition="An `if` condition attached to a `case`, e.g. `case x if x > 0:`, which must also be true for that case to match."),
        ],
        faq=[
            dict(q="Does Python have a do-while loop?", a="Not as a dedicated keyword. The idiomatic equivalent is `while True:` with a `break` condition at the point where you'd normally check the loop condition."),
            dict(q="Is match/case just a switch statement?", a="It's a superset of what switch does in most languages — beyond matching literal values, it can destructure tuples, dicts, and objects, and attach guard conditions, which C-style switch statements can't do."),
            dict(q="Why did my for-else block run even though I found what I was looking for?", a="You likely forgot the break statement in the matching branch — without break, Python has no way to know the loop 'succeeded', so the else clause runs regardless."),
        ],
        quiz=[
            dict(
                question="What does the else clause on a for loop run after?",
                options=["Every iteration", "Only if the loop completes without hitting break", "Only if the loop is empty", "Never, it's a syntax error"],
                correct=1,
                explanation="for...else's else block runs only when the loop finishes naturally, without break being called.",
            ),
            dict(
                question="Which of these values is falsy in an `if` check?",
                options=["'False' (the string)", "[0]", "0.0", "' ' (a space)"],
                correct=2,
                explanation="0.0 is falsy. The string 'False', the list [0], and a single-space string are all non-empty/non-zero and therefore truthy.",
            ),
        ],
        prompts=[
            "When should I use match/case instead of if/elif chains?",
            "Explain for-else with a real example of when it's actually useful.",
            "Why can't I break out of two nested loops with one break statement, and what's the idiomatic fix?",
            "What values in Python are considered falsy?",
            "Show me a match/case example that destructures a dictionary.",
        ],
    ),
    dict(
        id="functions-and-scope",
        title="Functions & Scope (LEGB)",
        hook="Every name lookup in Python follows the same four-step search order — Local, Enclosing, Global, Built-in — and once that order clicks, 'UnboundLocalError' stops being mysterious.",
        explanation=(
            "A function is defined with `def`, can take positional and keyword parameters, and returns a value "
            "with `return` (or implicitly returns `None` if no `return` is reached). Functions are first-class "
            "objects in Python — they can be assigned to variables, passed as arguments, stored in data "
            "structures, and returned from other functions, which is the foundation for decorators, callbacks, "
            "and functional-style code.\n\n"
            "When Python looks up a name inside a function, it searches four scopes in order, commonly "
            "abbreviated LEGB: Local (names assigned inside the current function), Enclosing (names in any "
            "enclosing function, for nested functions), Global (names at module level), and Built-in (names "
            "like `len` or `print` that Python provides everywhere). The search stops at the first scope where "
            "the name is found.\n\n"
            "A critical rule trips up nearly everyone at some point: if a name is assigned anywhere inside a "
            "function, Python treats that name as local to the *entire* function body, even before the "
            "assignment line. This means reading a variable before assigning to it later in the same function "
            "raises `UnboundLocalError`, not a fallback to a same-named global variable — Python decided at "
            "compile time that this name belongs to the local scope.\n\n"
            "Default parameter values are evaluated exactly once, at function definition time, not on every "
            "call — which is fine for immutable defaults like `count=0` but a well-known trap for mutable ones "
            "like `items=[]`, since that same list object is reused across every call that doesn't supply its "
            "own."
        ),
        deep_dive=(
            "To intentionally modify a variable from an enclosing scope rather than creating a new local one, "
            "Python provides two keywords: `global` (to modify a module-level variable from inside a function) "
            "and `nonlocal` (to modify a variable from an enclosing *function's* scope, used in nested "
            "functions and closures). Without one of these declarations, any assignment inside a function "
            "creates a new local variable, full stop — there's no way to accidentally modify an outer variable "
            "through simple assignment.\n\n"
            "Keyword-only and positional-only parameters give fine control over how a function can be called. "
            "A `*` in the parameter list marks everything after it as keyword-only (`def f(a, *, b):` forces "
            "callers to write `f(1, b=2)`, rejecting `f(1, 2)`), which prevents ambiguous positional calls for "
            "functions with many boolean or optional flags. A `/` marks everything before it as positional-only "
            "(`def f(a, b, /):` forces `f(1, 2)`, rejecting `f(a=1, b=2)`), useful for parameter names that are "
            "implementation details, not part of the public API contract.\n\n"
            "Every function call in Python creates a new stack frame with its own local scope, which is why "
            "recursive functions work correctly — each recursive call gets independent local variables, even "
            "though they're all executing the same function body. Python's default recursion limit (usually "
            "1000, adjustable via `sys.setrecursionlimit`) exists because each frame consumes real memory and "
            "unbounded recursion would otherwise crash the interpreter rather than just the specific call."
        ),
        code=dict(
            lang="python",
            label="LEGB in action, and the UnboundLocalError trap",
            src=(
                "count = 0                     # global\n\n"
                "def increment():\n"
                "    count += 1                # UnboundLocalError!\n"
                "    return count\n\n"
                "def increment_fixed():\n"
                "    global count               # explicitly modify the global\n"
                "    count += 1\n"
                "    return count\n\n"
                "print(increment_fixed())       # 1\n"
                "print(increment_fixed())       # 2"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Keyword-only parameters and nonlocal in a closure",
            src=(
                "def configure(*, debug=False, retries=3):   # both keyword-only\n"
                "    return {\"debug\": debug, \"retries\": retries}\n\n"
                "configure(debug=True)          # OK\n"
                "# configure(True)              # TypeError: no positional args accepted\n\n"
                "def make_counter():\n"
                "    count = 0\n"
                "    def increment():\n"
                "        nonlocal count          # modify the ENCLOSING function's variable\n"
                "        count += 1\n"
                "        return count\n"
                "    return increment\n\n"
                "counter = make_counter()\n"
                "print(counter(), counter(), counter())   # 1 2 3"
            ),
        ),
        example=(
            "A configuration function with a dozen optional flags (`create_report(data, verbose=False, "
            "include_charts=True, format='pdf', ...)`) is made keyword-only after the required arguments, so "
            "every call site reads self-documenting (`create_report(data, format='csv')`) instead of a "
            "confusing string of unlabeled positional booleans."
        ),
        best_practices=[
            "Avoid `global` where possible — pass values in as arguments and return results instead of mutating shared module-level state.",
            "Use `*` to force keyword-only arguments for functions with more than two or three optional parameters, especially booleans.",
            "Keep functions focused on one task; a function needing many flags to change its behavior is often a sign it should be split into separate functions.",
            "Prefer returning new values over mutating arguments in place, unless the function's entire purpose is a well-documented in-place mutation (like `list.sort()`).",
            "Use `nonlocal` deliberately in closures when you need a nested function to update state in its enclosing function, rather than reaching for a mutable default or a class.",
        ],
        pitfalls=[
            "Reading a variable inside a function before assigning to it later in that same function, triggering `UnboundLocalError` because Python already decided the name is local.",
            "Forgetting `global` when a function is meant to modify a module-level variable, and being confused why the outer variable never changes.",
            "Writing deeply nested functions with several levels of closures, making the LEGB chain hard to reason about — usually a sign to refactor into a class or separate functions.",
            "Assuming positional and keyword arguments are interchangeable for every function, then being surprised when a keyword-only parameter rejects a positional call.",
        ],
        glossary=[
            dict(term="LEGB", definition="The order Python searches for a name: Local, Enclosing, Global, Built-in — stopping at the first scope where the name is found."),
            dict(term="Closure", definition="A nested function that 'remembers' variables from its enclosing function's scope even after that outer function has returned."),
            dict(term="global keyword", definition="Declares that an assignment inside a function should modify a module-level variable instead of creating a new local one."),
            dict(term="nonlocal keyword", definition="Declares that an assignment inside a nested function should modify a variable in the nearest enclosing function's scope, not create a new local one."),
            dict(term="Stack frame", definition="The block of memory holding one function call's local variables and execution state; each call (including each recursive call) gets its own frame."),
        ],
        faq=[
            dict(q="Why do I get UnboundLocalError even though the variable exists as a global?", a="Because you assign to that name somewhere later in the same function. Python decides at compile time that any name assigned anywhere in a function body is local for the whole function — it doesn't fall back to the global just because the read happens before the local assignment line."),
            dict(q="What's the real difference between global and nonlocal?", a="global reaches all the way to module-level scope. nonlocal reaches only to the nearest enclosing function scope (used for closures) and will raise a SyntaxError if there's no enclosing function scope with that variable."),
            dict(q="Can a function return more than one value?", a="Not literally, but `return a, b` packs the values into a tuple, and the caller can unpack it: `x, y = my_func()` — it looks like multiple return values but is really one tuple being unpacked."),
        ],
        quiz=[
            dict(
                question="What happens when this runs?\nx = 10\ndef f():\n    print(x)\n    x = 20\nf()",
                options=["Prints 10", "Prints 20", "UnboundLocalError", "Prints None"],
                correct=2,
                explanation="Because x is assigned inside f(), Python treats x as local for the whole function — the print(x) line runs before that local x has a value, raising UnboundLocalError.",
            ),
            dict(
                question="What does `def f(a, *, b):` require of callers?",
                options=["a and b must both be positional", "b must be passed as a keyword argument", "a is optional", "This is a syntax error"],
                correct=1,
                explanation="The bare * marks every following parameter as keyword-only, so f(1, 2) fails but f(1, b=2) works.",
            ),
        ],
        prompts=[
            "Why am I getting UnboundLocalError when the variable is clearly defined at the top of my file?",
            "Explain the difference between global and nonlocal with a closure example.",
            "When should I make function parameters keyword-only?",
            "What's a closure, and why would I use one instead of a class?",
            "Show me how Python's LEGB rule resolves a name inside three levels of nested functions.",
        ],
    ),
    dict(
        id="args-kwargs-unpacking",
        title="*args, **kwargs & Unpacking",
        hook="The single star and double star show up in three unrelated-looking places — function definitions, function calls, and assignment — and it's the same underlying idea every time: 'gather' or 'spread' a group of values.",
        explanation=(
            "In a function definition, `*args` collects any extra positional arguments into a tuple, and "
            "`**kwargs` collects any extra keyword arguments into a dict. This lets a function accept a "
            "variable number of arguments without the caller needing to pass a list or dict explicitly: "
            "`def total(*numbers): return sum(numbers)` accepts `total(1, 2, 3)` or `total(1, 2, 3, 4, 5)` "
            "equally well.\n\n"
            "In a function *call*, the same `*` and `**` do the opposite job: they unpack an existing "
            "collection into separate arguments. `my_func(*my_list)` spreads each element of `my_list` out as "
            "its own positional argument, and `my_func(**my_dict)` spreads each key-value pair out as a "
            "keyword argument (the dict's keys must be valid parameter names as strings).\n\n"
            "Unpacking also works in plain assignment, independent of functions entirely: `first, *rest = "
            "[1, 2, 3, 4]` assigns `1` to `first` and `[2, 3, 4]` to `rest` — the starred name gathers "
            "'everything else' into a list, and it can appear in any position: `*start, last = [1, 2, 3, 4]` "
            "gives `start = [1, 2, 3]` and `last = 4`.\n\n"
            "The names `args` and `kwargs` are just convention, not syntax — `*values` and `**options` work "
            "identically. What matters is the `*` and `**` themselves; the name after them is your choice, the "
            "same as any other parameter name."
        ),
        deep_dive=(
            "Parameter order in a function definition is fixed: standard positional parameters, then "
            "`*args`, then keyword-only parameters, then `**kwargs` — `def f(a, b, *args, c, d=5, **kwargs):` "
            "is valid and each section behaves according to its own rules (a and b positional-or-keyword, args "
            "gathers extra positional, c is required keyword-only, d is optional keyword-only, kwargs gathers "
            "extra keyword arguments).\n\n"
            "A common, genuinely powerful pattern is a wrapper function that forwards whatever it receives to "
            "another function unchanged: `def logged(*args, **kwargs): print(args, kwargs); return "
            "original(*args, **kwargs)`. This is exactly how decorators (covered separately) wrap arbitrary "
            "functions without needing to know their specific signature in advance.\n\n"
            "Dict unpacking with `**` also merges dictionaries concisely: `merged = {**defaults, **overrides}` "
            "creates a new dict where any key present in both takes the value from `overrides`, since later "
            "unpacking overwrites earlier keys of the same name. This is the modern, readable alternative to "
            "manually looping and updating a copy."
        ),
        code=dict(
            lang="python",
            label="Gathering with *args/**kwargs, spreading at the call site",
            src=(
                "def describe(name, *hobbies, **extra_info):\n"
                "    print(f\"{name} enjoys: {hobbies}\")\n"
                "    print(f\"Extra: {extra_info}\")\n\n"
                "describe(\"Amara\", \"chess\", \"hiking\", city=\"Nairobi\", age=29)\n"
                "# Amara enjoys: ('chess', 'hiking')\n"
                "# Extra: {'city': 'Nairobi', 'age': 29}\n\n"
                "args = [\"chess\", \"hiking\"]\n"
                "info = {\"city\": \"Nairobi\", \"age\": 29}\n"
                "describe(\"Amara\", *args, **info)         # same call, spread from collections"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Unpacking in assignment, and merging dicts",
            src=(
                "first, *middle, last = [1, 2, 3, 4, 5]\n"
                "print(first, middle, last)      # 1 [2, 3, 4] 5\n\n"
                "defaults = {\"retries\": 3, \"timeout\": 30}\n"
                "overrides = {\"timeout\": 60}\n"
                "config = {**defaults, **overrides}\n"
                "print(config)                    # {'retries': 3, 'timeout': 60}\n\n"
                "def forward_everything(*args, **kwargs):\n"
                "    return original_function(*args, **kwargs)   # a transparent pass-through wrapper"
            ),
        ),
        example=(
            "A `create_user(**kwargs)` function in a web framework accepts any combination of `email`, `name`, "
            "`is_admin`, and a dozen other optional fields without the function signature needing to list all "
            "of them explicitly — the caller passes exactly what they have, and the function reads what it "
            "needs from `kwargs`."
        ),
        best_practices=[
            "Use `*args`/`**kwargs` for genuinely variable-arity functions (like a logger or a wrapper), not as a substitute for a clear, explicit signature on a normal function.",
            "Prefer `{**a, **b}` for merging dictionaries over manual loops — it's a single readable expression.",
            "When forwarding arguments in a wrapper, always spread with `*args, **kwargs` to remain compatible with whatever the wrapped function's real signature is.",
            "Document what keys a function expects inside `**kwargs` if the set isn't self-evident — the signature alone won't show it.",
        ],
        pitfalls=[
            "Overusing `**kwargs` on functions that actually have a fixed, known set of parameters, which hides the real API from anyone reading the signature or using autocomplete.",
            "Forgetting that dict key order matters in `{**a, **b}` — the second dict's values win on key collisions, which is easy to get backwards.",
            "Passing a dict with non-string keys to `**` unpacking, which raises a TypeError since keyword arguments must be valid identifiers.",
        ],
        glossary=[
            dict(term="*args", definition="Gathers extra positional arguments into a tuple inside a function definition, or spreads a sequence into positional arguments at a call site."),
            dict(term="**kwargs", definition="Gathers extra keyword arguments into a dict inside a function definition, or spreads a dict into keyword arguments at a call site."),
            dict(term="Unpacking", definition="Spreading the contents of a list, tuple, or dict into separate values — usable in function calls and in plain assignment."),
            dict(term="Arity", definition="The number of arguments a function accepts; 'variable arity' means the function accepts a flexible number of arguments."),
        ],
        faq=[
            dict(q="Do I have to name them args and kwargs?", a="No — those are just convention. def f(*values, **options) works exactly the same way. What matters is the * and ** symbols, not the names after them."),
            dict(q="Can I use *args and **kwargs on the same function as normal parameters?", a="Yes, and it's common: def f(a, b, *args, **kwargs) — a and b are required, args gathers any extra positional arguments, kwargs gathers any extra keyword arguments."),
            dict(q="What's the difference between `*` unpacking a list and `**` unpacking a dict?", a="`*` spreads an iterable's items as positional arguments/values in order. `**` spreads a dict's key-value pairs as keyword arguments, and requires all keys to be strings."),
        ],
        quiz=[
            dict(
                question="What does `first, *rest = [10, 20, 30, 40]` assign to `rest`?",
                options=["20", "[20, 30, 40]", "[10, 20, 30, 40]", "40"],
                correct=1,
                explanation="The starred name gathers everything not captured by the other names into a list — here, everything after the first element.",
            ),
            dict(
                question="What does `{**{'a': 1}, **{'a': 2}}` evaluate to?",
                options=["{'a': 1}", "{'a': 2}", "Error", "{'a': [1, 2]}"],
                correct=1,
                explanation="Later unpacked dicts overwrite earlier keys of the same name, so the second 'a': 2 wins.",
            ),
        ],
        prompts=[
            "When should I use **kwargs versus explicit named parameters?",
            "Explain how *args and **kwargs let a decorator wrap any function regardless of its signature.",
            "Show me how to merge three dictionaries with later ones taking priority.",
            "What's the difference between unpacking in a function call versus in an assignment statement?",
        ],
    ),
    dict(
        id="oop-classes-and-objects",
        title="OOP Basics: Classes, Objects & self",
        hook="Every method you write in Python takes `self` as its first parameter — not because Python demands ceremony, but because that's literally how Python knows which object's data to work with.",
        explanation=(
            "A class is a blueprint for creating objects; `__init__` is the method Python calls automatically "
            "right after a new object is created, typically used to set up the object's initial attributes. "
            "`self` refers to the specific object a method is being called on — when you write `my_car.drive()`, "
            "Python effectively calls `Car.drive(my_car)` behind the scenes, which is why every instance "
            "method's first parameter receives the object itself.\n\n"
            "Instance attributes (set via `self.attribute = value`, usually inside `__init__`) belong to one "
            "specific object; each instance gets its own independent copy. Class attributes (defined directly "
            "in the class body, outside any method) are shared across every instance of the class unless a "
            "specific instance overrides them — this is a common source of the same 'mutable default' bug seen "
            "with function arguments, but at the class level.\n\n"
            "Methods are just functions defined inside a class body. Beyond regular instance methods, Python "
            "supports `@classmethod` (receives the class itself as the first argument, conventionally named "
            "`cls`, useful for alternate constructors) and `@staticmethod` (receives neither `self` nor `cls` — "
            "effectively a regular function that's just organized inside the class's namespace for "
            "discoverability)."
        ),
        deep_dive=(
            "`__init__` is not actually a constructor in the strictest sense — `__new__` is what actually "
            "creates the object, and `__init__` runs afterward to initialize it. For nearly all everyday "
            "classes you never need to touch `__new__`; it matters mainly for advanced patterns like "
            "singletons, immutable value types built on tuples, or metaclasses.\n\n"
            "Every attribute and method lookup on an instance checks the instance's own `__dict__` first, and "
            "falls back to the class (and then to any parent classes) if not found there — this is why "
            "reading a class attribute through an instance works even though it's not in that instance's own "
            "`__dict__`, but *writing* to it through an instance (`self.shared = new_value`) creates a new "
            "instance attribute that shadows the class attribute, rather than modifying the shared one.\n\n"
            "Properties (`@property`) let a method be accessed like a plain attribute (`obj.value` instead of "
            "`obj.value()`), which is the idiomatic way to add validation or computed behavior to attribute "
            "access without breaking existing code that already treats it as a plain attribute — you can start "
            "with a public attribute and convert it to a property later with zero changes to calling code."
        ),
        code=dict(
            lang="python",
            label="A class with instance attributes, a class attribute, and self",
            src=(
                "class BankAccount:\n"
                "    bank_name = \"FINESE Bank\"       # class attribute, shared by all instances\n\n"
                "    def __init__(self, owner, balance=0):\n"
                "        self.owner = owner            # instance attribute, unique per object\n"
                "        self.balance = balance\n\n"
                "    def deposit(self, amount):\n"
                "        self.balance += amount\n"
                "        return self.balance\n\n"
                "acc1 = BankAccount(\"Amara\", 100)\n"
                "acc2 = BankAccount(\"Kito\")\n"
                "acc1.deposit(50)\n"
                "print(acc1.balance, acc2.balance)   # 150 0 -- independent state"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="classmethod as an alternate constructor, and @property",
            src=(
                "class BankAccount:\n"
                "    def __init__(self, owner, balance=0):\n"
                "        self.owner = owner\n"
                "        self._balance = balance\n\n"
                "    @classmethod\n"
                "    def from_dict(cls, data):           # alternate constructor\n"
                "        return cls(data[\"owner\"], data[\"balance\"])\n\n"
                "    @property\n"
                "    def balance(self):\n"
                "        return self._balance\n\n"
                "    @balance.setter\n"
                "    def balance(self, value):\n"
                "        if value < 0:\n"
                "            raise ValueError(\"Balance can't go negative\")\n"
                "        self._balance = value\n\n"
                "acc = BankAccount.from_dict({\"owner\": \"Amara\", \"balance\": 100})\n"
                "acc.balance = 200          # calls the setter, validated\n"
                "# acc.balance = -50       # raises ValueError"
            ),
        ),
        example=(
            "A `Config` class using `@classmethod` alternate constructors (`Config.from_file(path)`, "
            "`Config.from_env()`, `Config.from_dict(data)`) gives callers several clear, self-documenting ways "
            "to build the same kind of object, all funneling into the same `__init__` internally."
        ),
        best_practices=[
            "Initialize every instance attribute inside `__init__` so an object's shape is predictable and documented in one place.",
            "Use `@classmethod` for alternate constructors instead of adding boolean flags to `__init__` to switch its behavior.",
            "Reach for `@staticmethod` only for methods that are logically related to the class but don't need `self` or `cls` at all — otherwise it's usually just a regular function.",
            "Use `@property` to add validation to an attribute without breaking existing code that reads or writes it as a plain attribute.",
            "Avoid mutable class attributes (like a list) unless you deliberately want that state shared across every instance.",
        ],
        pitfalls=[
            "Defining a mutable class attribute (`items = []`) expecting each instance to get its own list — every instance shares the exact same list object until one of them explicitly creates its own.",
            "Forgetting `self` as the first parameter of an instance method, which causes a confusing `TypeError` about the wrong number of arguments.",
            "Mutating `self._balance` directly from outside the class, bypassing a `@property` setter's validation logic entirely.",
        ],
        glossary=[
            dict(term="Instance attribute", definition="Data stored on a specific object, usually set via self.name = value inside __init__; independent per instance."),
            dict(term="Class attribute", definition="Data defined directly in the class body, shared by every instance unless an instance explicitly overrides it."),
            dict(term="self", definition="The conventional name for the first parameter of an instance method, automatically bound to the specific object the method was called on."),
            dict(term="classmethod", definition="A method bound to the class itself rather than an instance, conventionally taking `cls` as its first parameter — commonly used for alternate constructors."),
            dict(term="Property", definition="A method decorated with @property that's accessed like a plain attribute, letting you add logic (like validation) to attribute access transparently."),
        ],
        faq=[
            dict(q="Why does every method need `self` as the first parameter?", a="Because Python doesn't have implicit 'this' the way some languages do — obj.method(arg) is really Class.method(obj, arg) under the hood, so the method needs an explicit parameter to receive the object."),
            dict(q="What's the real difference between a classmethod and a staticmethod?", a="A classmethod receives the class itself (cls) as its first argument, so it can create or interact with instances of that class. A staticmethod receives neither self nor cls — it's just a regular function namespaced inside the class."),
            dict(q="When should I use @property instead of a plain attribute?", a="Start with a plain attribute. Convert it to a @property only when you need to add validation, computation, or logging to reading/writing it — the calling code doesn't need to change either way."),
        ],
        quiz=[
            dict(
                question="What happens if a class attribute is a mutable list and you don't override it per-instance?",
                options=["Each instance automatically gets its own copy", "Every instance shares the exact same list object", "It raises an error", "Python converts it to a tuple"],
                correct=1,
                explanation="Class attributes are shared across all instances unless a specific instance assigns its own value, shadowing the class attribute.",
            ),
            dict(
                question="What does obj.method(arg) actually translate to internally?",
                options=["method(arg)", "Class.method(obj, arg)", "obj.method(self, arg)", "It's unrelated to the class"],
                correct=1,
                explanation="Python passes the instance itself as the first argument (conventionally named self) to the method looked up on its class.",
            ),
        ],
        prompts=[
            "Why is my mutable class attribute shared across all my objects when I didn't want it to be?",
            "When should I use a classmethod instead of a regular __init__ parameter?",
            "Explain @property with a validation example.",
            "What's the difference between an instance attribute and a class attribute in practice?",
        ],
    ),
    dict(
        id="inheritance-and-dunder-methods",
        title="Inheritance & Dunder Methods",
        hook="The double-underscore methods (`__init__`, `__str__`, `__eq__`, `__len__`) are how your custom objects plug into Python's built-in syntax — write `__add__` and suddenly the `+` operator works on your class.",
        explanation=(
            "Inheritance lets a class (the subclass) reuse and extend another class's (the superclass's) "
            "behavior: `class Dog(Animal):` gives `Dog` every method and attribute `Animal` defines, which "
            "`Dog` can then override or add to. `super().__init__(...)` calls the parent class's version of a "
            "method — almost always used inside an overridden `__init__` to make sure the parent's setup still "
            "runs before the subclass adds its own.\n\n"
            "'Dunder' (double-underscore) methods are special methods Python calls automatically in response "
            "to built-in syntax and functions. `__init__` runs on object creation; `__str__` controls what "
            "`str(obj)` and `print(obj)` show; `__repr__` controls the unambiguous developer-facing "
            "representation (shown in a REPL or inside a list); `__eq__` controls what `==` does between two "
            "instances; `__len__` controls what `len(obj)` returns. Implementing the right dunder methods is "
            "what makes a custom class feel like a natural part of the language instead of a bolted-on object.\n\n"
            "Python supports multiple inheritance (`class C(A, B):`), resolved through the Method Resolution "
            "Order (MRO) — a deterministic algorithm (C3 linearization) that decides which parent's method wins "
            "when more than one defines the same name. `ClassName.__mro__` shows the exact order Python will "
            "search."
        ),
        deep_dive=(
            "`isinstance(obj, SomeClass)` checks whether an object is an instance of a class *or any of its "
            "subclasses*, which is almost always the right check for 'is this the kind of thing I expect', "
            "while `type(obj) is SomeClass` checks the exact type only, rejecting subclasses. This distinction "
            "matters for writing functions that should work correctly with subclasses of an expected type, "
            "following the Liskov Substitution Principle — a subclass should be usable anywhere its parent is "
            "expected without breaking the caller's assumptions.\n\n"
            "Python doesn't have true private attributes; a single leading underscore (`self._balance`) is "
            "purely a convention signaling 'internal, don't touch this from outside,' while a double leading "
            "underscore (`self.__balance`) triggers name mangling — Python internally renames it to "
            "`self._ClassName__balance`, which mainly exists to avoid accidental name collisions in subclasses, "
            "not to provide real access control.\n\n"
            "Abstract base classes (`from abc import ABC, abstractmethod`) let you define a class that can't "
            "be instantiated directly and requires subclasses to implement specific methods, enforced at "
            "instantiation time rather than only by convention or documentation — a useful tool for defining a "
            "genuine contract multiple implementations must follow."
        ),
        code=dict(
            lang="python",
            label="Inheritance with super(), and a custom __str__/__eq__",
            src=(
                "class Animal:\n"
                "    def __init__(self, name):\n"
                "        self.name = name\n\n"
                "    def speak(self):\n"
                "        return \"...\"\n\n"
                "class Dog(Animal):\n"
                "    def __init__(self, name, breed):\n"
                "        super().__init__(name)      # run Animal's setup first\n"
                "        self.breed = breed\n\n"
                "    def speak(self):\n"
                "        return \"Woof!\"\n\n"
                "    def __str__(self):\n"
                "        return f\"{self.name} the {self.breed}\"\n\n"
                "    def __eq__(self, other):\n"
                "        return isinstance(other, Dog) and self.name == other.name\n\n"
                "d = Dog(\"Rex\", \"Labrador\")\n"
                "print(d)                    # Rex the Labrador (uses __str__)\n"
                "print(d.speak())            # Woof!"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="An abstract base class enforcing a contract",
            src=(
                "from abc import ABC, abstractmethod\n\n"
                "class PaymentMethod(ABC):\n"
                "    @abstractmethod\n"
                "    def charge(self, amount):\n"
                "        ...\n\n"
                "class CreditCard(PaymentMethod):\n"
                "    def charge(self, amount):\n"
                "        return f\"Charged ${amount} to credit card\"\n\n"
                "# PaymentMethod()          # TypeError: can't instantiate abstract class\n"
                "card = CreditCard()\n"
                "print(card.charge(50))      # Charged $50 to credit card\n"
                "print(isinstance(card, PaymentMethod))   # True"
            ),
        ),
        example=(
            "A `Shape` base class with an abstract `area()` method, subclassed by `Circle` and `Rectangle`, "
            "lets a function like `total_area(shapes: list[Shape])` sum areas across a mixed list without "
            "caring which concrete shape each one is — it just trusts the contract that every `Shape` "
            "implements `area()`."
        ),
        best_practices=[
            "Call `super().__init__(...)` in every subclass `__init__` that overrides it, so the parent's setup still runs.",
            "Prefer `isinstance()` over `type() is` for type checks, unless you specifically need to exclude subclasses.",
            "Implement `__repr__` on custom classes even if you also implement `__str__` — it makes debugging in a REPL or logs far easier.",
            "Use abstract base classes when you want to guarantee, at instantiation time, that every subclass implements specific methods.",
            "Favor composition (one class holding an instance of another) over deep inheritance chains when the relationship isn't a genuine 'is-a' relationship.",
        ],
        pitfalls=[
            "Overriding `__init__` in a subclass and forgetting to call `super().__init__()`, silently skipping the parent class's setup.",
            "Implementing `__eq__` without also implementing `__hash__`, which makes instances unusable as dict keys or set members (Python sets `__hash__` to None automatically when you define `__eq__` without it).",
            "Building deep, multi-level inheritance hierarchies for convenience, making the actual behavior of a leaf class hard to trace without reading every ancestor.",
            "Assuming double-underscore attributes are truly private — name mangling prevents accidental collisions, not deliberate access.",
        ],
        glossary=[
            dict(term="Superclass / subclass", definition="The superclass (or parent/base class) is inherited from; the subclass (or child/derived class) inherits and can extend or override its behavior."),
            dict(term="super()", definition="A proxy object that lets a subclass call a method from its parent class, most commonly super().__init__(...)."),
            dict(term="Dunder method", definition="A 'double underscore' special method (like __init__, __str__, __eq__) that Python calls automatically for built-in syntax and functions."),
            dict(term="MRO (Method Resolution Order)", definition="The deterministic order Python searches through a class's ancestors when looking up a method, especially relevant with multiple inheritance."),
            dict(term="Abstract base class", definition="A class that can't be instantiated directly and defines methods subclasses are required to implement, enforced via the abc module."),
        ],
        faq=[
            dict(q="What's the difference between __str__ and __repr__?", a="__str__ is meant to be a readable, user-facing string (used by print() and str()). __repr__ is meant to be an unambiguous, developer-facing representation, ideally one that could recreate the object. If __str__ isn't defined, Python falls back to __repr__."),
            dict(q="Why did defining __eq__ break using my objects as dict keys?", a="Python automatically sets __hash__ to None when you define __eq__ without also defining __hash__, because two 'equal' objects must have the same hash for dicts/sets to work correctly — you need to implement both together."),
            dict(q="Can a Python class inherit from more than one class?", a="Yes, multiple inheritance is supported (class C(A, B):), with method lookup resolved by the MRO. It's powerful but can get confusing quickly, so many style guides recommend using it sparingly, often via small, focused mixin classes."),
        ],
        quiz=[
            dict(
                question="What does super().__init__() do inside a subclass's __init__?",
                options=["Creates a new object", "Calls the parent class's __init__ method", "Deletes the parent class", "Nothing, it's optional syntax"],
                correct=1,
                explanation="super() gives access to the parent class's methods, and calling __init__ through it runs the parent's setup logic.",
            ),
            dict(
                question="Why must __hash__ be defined alongside __eq__ for objects to work correctly in a set?",
                options=["It's not actually required", "Two equal objects must produce the same hash value for set/dict lookups to behave correctly", "Python requires all classes to be hashable", "__hash__ controls how __eq__ is called"],
                correct=1,
                explanation="Sets and dicts rely on hash equality to find matching entries efficiently — if equal objects had different hashes, lookups would be inconsistent, so Python disables the default hash once you override __eq__.",
            ),
        ],
        prompts=[
            "Why did my subclass's __init__ not run the parent class's setup logic?",
            "Explain the difference between __str__ and __repr__ with an example.",
            "When should I use an abstract base class versus just documenting a convention?",
            "Show me how Python resolves a method call with multiple inheritance.",
        ],
    ),
    dict(
        id="comprehensions-and-generators",
        title="Comprehensions & Generators",
        hook="A list comprehension and a generator expression can look almost identical — swap square brackets for parentheses — but one builds the whole result immediately and the other builds nothing until you ask for the next item.",
        explanation=(
            "A list comprehension (`[x**2 for x in range(10)]`) builds a complete list in one expression, "
            "replacing the more verbose pattern of creating an empty list and appending inside a loop. Dict "
            "and set comprehensions follow the same shape with different brackets: `{k: v for k, v in "
            "pairs}` and `{x for x in items}`. All comprehensions support an optional filtering clause "
            "(`[x for x in nums if x % 2 == 0]`) and can be nested for multi-dimensional data.\n\n"
            "A generator expression (`(x**2 for x in range(10))`) looks nearly identical but produces a "
            "generator object instead of a list — it computes each value lazily, on demand, as you iterate, "
            "rather than building the entire sequence upfront. This makes generators dramatically more "
            "memory-efficient for large or even infinite sequences, at the cost of only being iterable once.\n\n"
            "The `yield` keyword turns an ordinary function into a generator function. Instead of computing "
            "and returning a full result, each call to `next()` on the generator runs the function until it "
            "hits a `yield`, returns that value, and pauses — remembering exactly where it left off for the "
            "next call. This lets you express arbitrarily complex lazy sequences (not just simple "
            "transformations of an existing iterable) as ordinary-looking function code.\n\n"
            "A generator is a specific kind of iterator, and an iterator is anything implementing the iterator "
            "protocol (`__iter__` and `__next__`). `for` loops, list(), and every other place Python consumes "
            "an iterable work identically whether given a list, a generator, or a custom iterator class — the "
            "consuming code never needs to know which one it received."
        ),
        deep_dive=(
            "Because a generator computes values one at a time and never stores the full sequence, iterating "
            "over it a second time yields nothing — once exhausted, a generator is permanently spent, and "
            "you'd need to call the generator function again to get a fresh one. This is a common source of "
            "confusing bugs: code that works the first time (`for x in gen: ...`) silently does nothing the "
            "second time it runs the same loop over the same, already-exhausted generator object.\n\n"
            "Generator functions can also receive values sent back into them with `.send(value)`, and can "
            "delegate to another generator entirely with `yield from`, which is the idiomatic way to compose "
            "generators — `yield from sub_generator()` re-yields every value the sub-generator produces "
            "without an explicit loop, and also correctly forwards `.send()` and exceptions.\n\n"
            "For a rough intuition of when a generator wins: if you're going to consume the entire sequence "
            "and it's small, a list comprehension is simpler and just as fast. If the sequence is large, "
            "possibly infinite, or you might stop consuming it early (like searching for the first match), a "
            "generator avoids doing (or storing) work you'll never use."
        ),
        code=dict(
            lang="python",
            label="List, dict, and set comprehensions",
            src=(
                "squares = [x**2 for x in range(10) if x % 2 == 0]\n"
                "print(squares)                       # [0, 4, 16, 36, 64]\n\n"
                "word_lengths = {word: len(word) for word in [\"hi\", \"hello\", \"hey\"]}\n"
                "print(word_lengths)                  # {'hi': 2, 'hello': 5, 'hey': 3}\n\n"
                "unique_first_letters = {word[0] for word in [\"cat\", \"car\", \"dog\"]}\n"
                "print(unique_first_letters)          # {'c', 'd'}"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="A generator function with yield, and yield from",
            src=(
                "def fibonacci(limit):\n"
                "    a, b = 0, 1\n"
                "    while a < limit:\n"
                "        yield a               # pause here, return a, resume on next()\n"
                "        a, b = b, a + b\n\n"
                "for n in fibonacci(20):\n"
                "    print(n, end=\" \")          # 0 1 1 2 3 5 8 13\n\n"
                "def flatten(nested):\n"
                "    for item in nested:\n"
                "        if isinstance(item, list):\n"
                "            yield from flatten(item)    # delegate to a recursive sub-generator\n"
                "        else:\n"
                "            yield item\n\n"
                "print(list(flatten([1, [2, 3, [4, 5]], 6])))   # [1, 2, 3, 4, 5, 6]"
            ),
        ),
        example=(
            "Reading a 50GB log file line by line with `(line for line in open(path) if 'ERROR' in line)` "
            "processes it in constant memory regardless of file size, while `[line for line in open(path) if "
            "'ERROR' in line]` would try to load every matching line into memory simultaneously."
        ),
        best_practices=[
            "Default to a generator expression over a list comprehension whenever you're going to iterate once and don't need indexing, length, or multiple passes.",
            "Keep comprehensions to one or two clauses (one loop, one optional filter) — anything more nested is usually clearer as a regular loop.",
            "Use `yield from` when a generator needs to delegate to another generator, instead of manually looping and yielding each value.",
            "Remember a generator is single-use; if you need to iterate multiple times, either convert it to a list (`list(gen)`) once, or call the generator function again for a fresh one.",
        ],
        pitfalls=[
            "Iterating over the same generator object twice and getting nothing the second time, without realizing it's already exhausted.",
            "Writing a deeply nested comprehension with multiple loops and conditions that's genuinely harder to read than the equivalent explicit for loop.",
            "Building a giant list comprehension purely to iterate over it once and discard it, when a generator expression would do the same job with far less memory.",
        ],
        glossary=[
            dict(term="Comprehension", definition="A concise expression that builds a list, dict, or set from an iterable in one line, optionally filtered by a condition."),
            dict(term="Generator expression", definition="Syntactically like a list comprehension but with parentheses, producing a lazy generator instead of a fully built list."),
            dict(term="yield", definition="A keyword that pauses a generator function, returns a value to the caller, and resumes execution from that exact point on the next call to next()."),
            dict(term="Lazy evaluation", definition="Computing values only when they're actually needed, rather than all at once upfront — the defining trait of generators."),
            dict(term="Iterator protocol", definition="The __iter__ and __next__ methods that make an object usable in a for loop and with next()."),
        ],
        faq=[
            dict(q="Why did my second for loop over the same generator do nothing?", a="Generators are single-use — once exhausted (either by a full loop or by calling next() until StopIteration), there's nothing left to produce. Call the generator function again to get a fresh generator object."),
            dict(q="Is a generator expression always faster than a list comprehension?", a="Not necessarily in raw speed for small data — the real win is memory. For large or infinite sequences, a generator avoids building the whole thing in memory; for small sequences you'll fully consume anyway, the difference is negligible."),
            dict(q="What's the difference between `return` and `yield` inside the same function?", a="A function can't meaningfully mix them for the same value — using yield anywhere in a function body makes the whole function a generator function. A `return` inside a generator function just stops iteration (raises StopIteration) rather than returning a value the normal way."),
        ],
        quiz=[
            dict(
                question="What does `(x for x in range(5))` create?",
                options=["A list", "A tuple", "A generator object", "A set"],
                correct=2,
                explanation="Parentheses around a comprehension-like expression create a generator expression, producing a generator object, not a tuple.",
            ),
            dict(
                question="What happens if you iterate over an already-exhausted generator?",
                options=["It restarts from the beginning", "It raises a TypeError", "The loop body simply never executes", "It returns the last value again"],
                correct=2,
                explanation="An exhausted generator immediately raises StopIteration on next(), which a for loop interprets as 'nothing left' and simply doesn't execute its body.",
            ),
        ],
        prompts=[
            "When should I use a generator instead of a list comprehension?",
            "Why does looping over my generator a second time produce nothing?",
            "Explain yield from with a recursive flattening example.",
            "Convert this nested for loop into a list comprehension, or explain why I shouldn't.",
        ],
    ),
    dict(
        id="decorators-and-context-managers",
        title="Decorators & Context Managers",
        hook="The @ symbol above a function definition and the `with` statement both solve the same underlying problem — wrapping some behavior around code you don't want to repeat — just at different scales.",
        explanation=(
            "A decorator is a function that takes another function as input and returns a new function that "
            "usually wraps the original with extra behavior — logging, timing, caching, access control — "
            "without modifying the original function's own code. `@my_decorator` above a function definition "
            "is exactly equivalent to writing `my_func = my_decorator(my_func)` right after defining it; the "
            "`@` syntax is pure sugar for that reassignment pattern.\n\n"
            "A minimal decorator is a function returning a function: the outer function receives the original "
            "function, defines an inner `wrapper` function that calls the original (plus whatever extra logic "
            "you want), and returns that wrapper. `functools.wraps` should be applied to the wrapper to "
            "preserve the original function's name, docstring, and metadata — without it, tools like help() "
            "and debuggers see the generic wrapper instead of the real function.\n\n"
            "A context manager handles setup and guaranteed cleanup around a block of code, used with the "
            "`with` statement: `with open(\"file.txt\") as f:` guarantees the file gets closed even if an "
            "exception occurs inside the block, without needing an explicit `try/finally`. Any object "
            "implementing `__enter__` (setup, returns the value bound by `as`) and `__exit__` (cleanup, always "
            "runs) can be used this way.\n\n"
            "The `contextlib.contextmanager` decorator lets you write a context manager as a generator function "
            "instead of a full class — code before the `yield` runs as `__enter__`, the yielded value is what "
            "`as` binds to, and code after the `yield` runs as `__exit__` (wrapped in a try/finally so cleanup "
            "still happens if the block raises)."
        ),
        deep_dive=(
            "Decorators can themselves accept arguments, which requires an extra layer of nesting: a decorator "
            "factory function that takes the arguments and returns the actual decorator, which then takes the "
            "function and returns the wrapper. `@retry(times=3)` above a function means `retry(times=3)` runs "
            "first (returning the real decorator), which is then applied to the function — three levels of "
            "functions deep, which is genuinely one of the more mind-bending patterns in everyday Python but "
            "becomes mechanical once you've written it a few times.\n\n"
            "Multiple decorators stack in the order they're written, applied bottom-up: `@a` then `@b` above a "
            "function means `b` wraps the function first, then `a` wraps the result of that — so at call time, "
            "`a`'s wrapper logic runs first (outermost), calling into `b`'s wrapper, which calls the original "
            "function.\n\n"
            "`__exit__` receives the exception type, value, and traceback if the `with` block raised one "
            "(all `None` if it completed normally), and can return `True` to suppress that exception entirely "
            "— swallowing it rather than letting it propagate. This is powerful for building context managers "
            "that gracefully handle specific expected errors, but returning `True` unconditionally is a common "
            "and dangerous mistake that silently hides real bugs."
        ),
        code=dict(
            lang="python",
            label="A timing decorator with functools.wraps",
            src=(
                "import functools, time\n\n"
                "def timed(func):\n"
                "    @functools.wraps(func)              # preserves func's name/docstring\n"
                "    def wrapper(*args, **kwargs):\n"
                "        start = time.perf_counter()\n"
                "        result = func(*args, **kwargs)\n"
                "        elapsed = time.perf_counter() - start\n"
                "        print(f\"{func.__name__} took {elapsed:.4f}s\")\n"
                "        return result\n"
                "    return wrapper\n\n"
                "@timed\n"
                "def slow_add(a, b):\n"
                "    time.sleep(0.1)\n"
                "    return a + b\n\n"
                "slow_add(2, 3)   # prints: slow_add took 0.1002s"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="A parameterized decorator, and a generator-based context manager",
            src=(
                "def retry(times):\n"
                "    def decorator(func):\n"
                "        @functools.wraps(func)\n"
                "        def wrapper(*args, **kwargs):\n"
                "            for attempt in range(times):\n"
                "                try:\n"
                "                    return func(*args, **kwargs)\n"
                "                except Exception as e:\n"
                "                    print(f\"Attempt {attempt+1} failed: {e}\")\n"
                "            raise RuntimeError(\"All retries failed\")\n"
                "        return wrapper\n"
                "    return decorator\n\n"
                "@retry(times=3)\n"
                "def flaky_call():\n"
                "    ...\n\n"
                "from contextlib import contextmanager\n\n"
                "@contextmanager\n"
                "def timer(label):\n"
                "    start = time.perf_counter()\n"
                "    yield                    # code inside the `with` block runs here\n"
                "    print(f\"{label}: {time.perf_counter() - start:.4f}s\")\n\n"
                "with timer(\"database query\"):\n"
                "    time.sleep(0.2)"
            ),
        ),
        example=(
            "A Flask route protected with `@login_required` above the view function is a decorator checking "
            "the request's session before letting the original function run at all, returning a 401 response "
            "immediately if the check fails — the route function itself never needs to contain that "
            "authentication logic."
        ),
        best_practices=[
            "Always apply `functools.wraps(func)` to a decorator's inner wrapper function to preserve the original's name and docstring.",
            "Use `contextlib.contextmanager` for simple setup/teardown context managers instead of writing a full class with `__enter__`/`__exit__`.",
            "Keep decorators focused on one cross-cutting concern (logging, timing, retrying, caching) rather than bundling unrelated behavior into one decorator.",
            "Be explicit and cautious about what `__exit__` returns — only return True when you genuinely intend to suppress a specific, expected exception type.",
        ],
        pitfalls=[
            "Forgetting `functools.wraps`, which leaves every decorated function reporting the wrapper's generic name and no docstring in tools like `help()`.",
            "Writing a decorator that doesn't accept `*args, **kwargs`, breaking the moment it's applied to a function with a different signature than the one it was tested against.",
            "Returning `True` from `__exit__` unconditionally, silently swallowing every exception raised inside the `with` block, including genuine bugs.",
            "Stacking decorators without understanding the bottom-up application order, then being confused about which wrapper's logic runs first.",
        ],
        glossary=[
            dict(term="Decorator", definition="A function that takes a function and returns a new function wrapping it with extra behavior, applied with the @decorator syntax."),
            dict(term="Higher-order function", definition="A function that takes another function as an argument, returns a function, or both — decorators are a specific application of this idea."),
            dict(term="Context manager", definition="An object implementing __enter__ and __exit__ (or a generator wrapped in @contextmanager) used with the `with` statement to guarantee setup and cleanup."),
            dict(term="functools.wraps", definition="A decorator applied to a wrapper function that copies over the original function's __name__, __doc__, and other metadata."),
        ],
        faq=[
            dict(q="What does @my_decorator actually do to the function below it?", a="It's shorthand for `my_func = my_decorator(my_func)` — the decorator function runs immediately at definition time, and whatever it returns replaces the original name."),
            dict(q="Why do I need three levels of nested functions for a decorator that takes arguments?", a="The outer function receives the decorator's arguments (like retry(times=3)) and must return the actual decorator function, which itself receives and wraps the target function, which itself returns the wrapper that runs at call time — each level has a distinct job."),
            dict(q="What's the advantage of @contextmanager over writing a class with __enter__/__exit__?", a="Less boilerplate for simple cases — you write ordinary sequential code with one yield marking the boundary between setup and teardown, instead of splitting the logic across two separate methods."),
        ],
        quiz=[
            dict(
                question="What is `@my_decorator` above a function definition equivalent to?",
                options=["my_decorator(my_func())", "my_func = my_decorator(my_func)", "my_func.decorate(my_decorator)", "It has no equivalent, it's unique syntax"],
                correct=1,
                explanation="The @ syntax is sugar for reassigning the function name to the result of calling the decorator on the original function.",
            ),
            dict(
                question="What does forgetting functools.wraps on a decorator's wrapper cause?",
                options=["The decorator stops working entirely", "The wrapped function's __name__ and docstring report the wrapper's, not the original's", "A SyntaxError at import time", "The original function's arguments are ignored"],
                correct=1,
                explanation="Without functools.wraps, introspection tools (help(), debuggers, some frameworks) see the generic wrapper's metadata instead of the original function's.",
            ),
        ],
        prompts=[
            "Write a decorator that caches a function's results based on its arguments.",
            "Explain why my decorator breaks when applied to a function with different arguments.",
            "Show me how to write a context manager using @contextmanager instead of a class.",
            "What's the correct order decorators run in when I stack three of them on one function?",
        ],
    ),
    dict(
        id="error-handling",
        title="Error Handling: try/except/else/finally",
        hook="Python's exception handling has four clauses, not two — and the two people usually forget (`else` and `finally`) are exactly the ones that make error-handling code correct instead of just functional-looking.",
        explanation=(
            "`try` wraps code that might raise an exception. `except ExceptionType:` catches a specific "
            "exception type (or a tuple of types) and runs recovery code. `else` runs only if the `try` block "
            "completed with no exception at all — useful for code that should run after success but that you "
            "don't want accidentally caught by the `except` block if it happens to raise the same exception "
            "type. `finally` always runs, whether or not an exception occurred, whether or not it was caught — "
            "the right place for guaranteed cleanup like closing a file or releasing a lock.\n\n"
            "Exceptions form a hierarchy: catching a parent class like `Exception` also catches every subclass "
            "of it, which is why `except Exception:` is a blunt instrument that catches nearly everything, "
            "including bugs you'd actually want to see crash loudly during development. Catching the most "
            "specific exception type that's actually expected (`except FileNotFoundError:` rather than "
            "`except Exception:`) keeps error handling precise and avoids silently swallowing unrelated bugs.\n\n"
            "`raise` re-raises the current exception (useful inside an `except` block after logging, to let it "
            "continue propagating), and `raise SomeError(\"message\") from original_error` explicitly chains a "
            "new exception to the one that caused it, preserving the full causal chain in the traceback rather "
            "than looking like an unrelated, spontaneous error.\n\n"
            "Custom exceptions are just classes inheriting from `Exception` (or a more specific built-in "
            "exception), letting you define application-specific error types (`class InsufficientFundsError"
            "(Exception): pass`) that calling code can catch precisely, rather than relying on generic "
            "exceptions or string-matching error messages."
        ),
        deep_dive=(
            "The `else` clause specifically exists to narrow what an `except` block is responsible for "
            "catching. Consider `try: value = risky_lookup() except KeyError: handle_missing() else: "
            "process(value)` — if `process(value)` itself happened to raise a `KeyError` for an unrelated "
            "reason, without `else` that error would be incorrectly caught by the same `except KeyError:` "
            "clause meant only for `risky_lookup()`. Moving success-path code into `else` ensures the `except` "
            "block only ever catches exceptions from the code it was actually written to guard.\n\n"
            "`finally` runs even if the `try` or `except` block executes a `return`, `break`, or `continue` — "
            "Python holds that pending control-flow action, runs the entire `finally` block, and only then "
            "actually returns/breaks/continues. This makes `finally` genuinely reliable for cleanup even in "
            "the presence of early returns, though a `return` inside `finally` itself will silently override "
            "and discard any pending return value or exception from the try block, which is a subtle, "
            "generally-considered-bad-practice trap.\n\n"
            "Custom exception hierarchies are worth designing deliberately for any non-trivial application: a "
            "base `AppError(Exception)` with specific subclasses (`ValidationError`, `NotFoundError`, "
            "`PermissionError`) lets calling code choose its granularity — catch the specific subclass for "
            "precise handling, or catch the shared base class to handle 'any error from my application' in "
            "one place, like a top-level API error handler."
        ),
        code=dict(
            lang="python",
            label="try/except/else/finally, each clause doing its distinct job",
            src=(
                "def read_config(path):\n"
                "    try:\n"
                "        f = open(path)\n"
                "    except FileNotFoundError:\n"
                "        print(f\"{path} not found, using defaults\")\n"
                "        return {}\n"
                "    else:\n"
                "        data = f.read()          # only runs if open() succeeded\n"
                "        f.close()\n"
                "        return parse(data)\n"
                "    finally:\n"
                "        print(\"Attempted to read config\")   # always runs"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="A custom exception hierarchy with exception chaining",
            src=(
                "class AppError(Exception):\n"
                "    \"\"\"Base class for all application-specific errors.\"\"\"\n\n"
                "class InsufficientFundsError(AppError):\n"
                "    def __init__(self, balance, amount):\n"
                "        super().__init__(f\"Balance {balance} is less than requested {amount}\")\n"
                "        self.balance = balance\n"
                "        self.amount = amount\n\n"
                "def withdraw(balance, amount):\n"
                "    try:\n"
                "        if amount > balance:\n"
                "            raise InsufficientFundsError(balance, amount)\n"
                "        return balance - amount\n"
                "    except ValueError as e:\n"
                "        raise AppError(\"Withdrawal failed\") from e   # chain the original cause\n\n"
                "try:\n"
                "    withdraw(100, 150)\n"
                "except InsufficientFundsError as e:\n"
                "    print(f\"Caught: {e}\")   # Balance 100 is less than requested 150"
            ),
        ),
        example=(
            "An API endpoint catches a specific `ValidationError` to return a 400 response with a helpful "
            "message, lets an unexpected `Exception` propagate to a top-level handler that logs it and returns "
            "a generic 500, and uses `finally` to always release a database connection back to the pool "
            "regardless of which path was taken."
        ),
        best_practices=[
            "Catch the most specific exception type you actually expect, rather than a bare `except Exception:` or, worse, a bare `except:`.",
            "Use `else` for success-path code that shouldn't accidentally be caught by the same `except` block.",
            "Use `finally` (or a context manager) for guaranteed cleanup, not just an assumption that the happy path will always reach your cleanup code.",
            "Chain exceptions with `raise NewError(...) from original` when translating a low-level error into a higher-level one, to preserve the real cause in the traceback.",
            "Design a small custom exception hierarchy for any application with more than a couple of distinct failure modes, rather than raising generic exceptions everywhere.",
        ],
        pitfalls=[
            "Using a bare `except:` (no exception type at all), which catches even `KeyboardInterrupt` and `SystemExit`, making the program impossible to stop cleanly.",
            "Catching `Exception` broadly 'just in case,' which hides real bugs and makes them far harder to notice and debug.",
            "Putting a `return` statement inside a `finally` block, which silently discards any exception or return value from the try/except blocks.",
            "Swallowing an exception with `except Exception: pass`, losing all information about what actually went wrong.",
        ],
        glossary=[
            dict(term="Exception hierarchy", definition="The inheritance tree of exception classes; catching a parent class also catches all its subclasses."),
            dict(term="Exception chaining", definition="Using `raise NewError(...) from original_error` to preserve the causal link between a low-level error and a higher-level one raised in response to it."),
            dict(term="Bare except", definition="An `except:` clause with no exception type specified, which catches literally everything, including exceptions meant to stop the program — almost always a mistake."),
            dict(term="Custom exception", definition="An application-defined exception class, typically inheriting from Exception or a more specific built-in, used to represent domain-specific failure modes."),
        ],
        faq=[
            dict(q="What's the point of the else clause if I could just put that code at the end of the try block?", a="Putting it in try means an exception raised by that success-path code could be mistakenly caught by an except clause meant for a different, earlier operation. else code only runs after the try block fully succeeds, and is never itself subject to the except clauses above it."),
            dict(q="Does finally run if the try block has a return statement?", a="Yes — Python holds the pending return value, runs the finally block completely, and only then actually returns. If finally itself has a return, it overrides and discards the original one, which is a common gotcha."),
            dict(q="When should I define a custom exception instead of raising a built-in one?", a="When the failure is specific to your application's domain (like InsufficientFundsError) and callers would benefit from catching that specific case separately from generic errors like ValueError or KeyError."),
        ],
        quiz=[
            dict(
                question="Which clause runs only if the try block completes with no exception?",
                options=["except", "else", "finally", "raise"],
                correct=1,
                explanation="else runs only on a successful try block, and unlike code placed inside try, it isn't subject to being caught by the except clauses above it.",
            ),
            dict(
                question="What's wrong with a bare `except:` clause?",
                options=["It's a syntax error", "It catches every exception including KeyboardInterrupt and SystemExit", "It only catches ValueError", "Nothing, it's the recommended default"],
                correct=1,
                explanation="A bare except catches everything, including exceptions meant to let a user interrupt or the program exit, which can make a program impossible to stop and hides real bugs.",
            ),
        ],
        prompts=[
            "Why would I use else instead of just putting that code inside the try block?",
            "Design a custom exception hierarchy for a simple e-commerce checkout flow.",
            "Explain exception chaining with `raise ... from ...` and why it matters for debugging.",
            "What's actually wrong with catching Exception broadly, if it technically works?",
        ],
    ),
    dict(
        id="file-io-and-modules",
        title="File I/O & the Module System",
        hook="`with open(...)` isn't just a style preference over manually calling `.close()` — it's the difference between code that reliably releases file handles and code that leaks them the moment an exception happens.",
        explanation=(
            "`open(path, mode)` returns a file object; common modes are `\"r\"` (read text, default), `\"w\"` "
            "(write, overwriting), `\"a\"` (append), and adding `\"b\"` for binary mode (`\"rb\"`, `\"wb\"`). Using "
            "`open()` as a context manager (`with open(path) as f:`) guarantees the file is closed when the "
            "block exits, even if an exception is raised inside it — manually calling `f.close()` after your "
            "code means that close never happens if something raises before reaching that line.\n\n"
            "Reading a file can be done a full line at a time by iterating directly over the file object "
            "(`for line in f:`), which is memory-efficient even for huge files since it reads incrementally "
            "rather than loading everything at once, or all at once with `f.read()` (whole file as one "
            "string) or `f.readlines()` (list of lines) when the file is small enough that memory isn't a "
            "concern.\n\n"
            "The `pathlib` module (`from pathlib import Path`) is the modern, object-oriented way to work with "
            "filesystem paths, replacing most uses of the older `os.path` string-based functions: `Path(\"data\") "
            "/ \"file.csv\"` builds a path with the `/` operator instead of string concatenation, and works "
            "correctly across both Windows and Unix path separators automatically.\n\n"
            "Python's import system treats every `.py` file as a module and every directory containing an "
            "`__init__.py` (or, since Python 3.3, even without one, as a 'namespace package') as a package. "
            "`import module_name` runs that module's top-level code once and caches the result in `sys.modules` "
            "— importing it again elsewhere in the same program reuses the cached module rather than "
            "re-executing it."
        ),
        deep_dive=(
            "Text mode (`\"r\"`) automatically decodes bytes to `str` using an encoding (defaulting to the "
            "platform's preferred encoding, which is not guaranteed to be UTF-8 on every system) and "
            "translates line endings; binary mode (`\"rb\"`) returns raw `bytes` with no decoding or "
            "translation at all. Explicitly passing `encoding=\"utf-8\"` to `open()` is considered a best "
            "practice specifically because relying on the platform default can make code behave differently "
            "on different machines — a frequent source of 'it works on my computer' bugs around file I/O.\n\n"
            "Relative imports (`from . import sibling_module`, `from ..package import thing`) only work "
            "inside a package (a directory Python recognizes as such) and are resolved relative to the "
            "importing module's own package, not the current working directory the script happens to be run "
            "from — a common source of confusion when a script that works when run one way fails with an "
            "`ImportError` when run a different way.\n\n"
            "The `if __name__ == \"__main__\":` guard exists because every module has a `__name__` attribute "
            "set to `\"__main__\"` only when that file is executed directly, and set to the module's actual "
            "name when it's imported by something else. Wrapping a script's 'run this when executed directly' "
            "logic in that guard lets the same file be both a reusable, importable module and a standalone "
            "script, without the import triggering unwanted side effects."
        ),
        code=dict(
            lang="python",
            label="Reading and writing files safely with context managers",
            src=(
                "from pathlib import Path\n\n"
                "path = Path(\"data\") / \"notes.txt\"\n\n"
                "with open(path, \"w\", encoding=\"utf-8\") as f:\n"
                "    f.write(\"first line\\n\")\n"
                "    f.write(\"second line\\n\")\n\n"
                "with open(path, \"r\", encoding=\"utf-8\") as f:\n"
                "    for line in f:                 # memory-efficient, one line at a time\n"
                "        print(line.strip())\n\n"
                "print(path.exists(), path.stat().st_size)"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="The __name__ == '__main__' guard and a relative import",
            src=(
                "# mypackage/utils.py\n"
                "def helper():\n"
                "    return \"helper result\"\n\n"
                "# mypackage/main.py\n"
                "from .utils import helper          # relative import, only works inside the package\n\n"
                "def run():\n"
                "    print(helper())\n\n"
                "if __name__ == \"__main__\":         # only runs when this file is executed directly\n"
                "    run()                           # NOT when main.py is imported elsewhere"
            ),
        ),
        example=(
            "A data pipeline script processing a 20GB CSV uses `for line in open(path):` to stream through it "
            "one line at a time in constant memory, where calling `.read()` or `.readlines()` on the whole "
            "file upfront would try to load the entire 20GB into RAM at once."
        ),
        best_practices=[
            "Always use `with open(...) as f:` instead of manual `open()`/`close()` pairs — it guarantees the file closes even on an exception.",
            "Pass `encoding=\"utf-8\"` explicitly when opening text files, rather than relying on the platform's default encoding.",
            "Prefer `pathlib.Path` over raw string concatenation for building filesystem paths — it's cross-platform correct by construction.",
            "Wrap a script's direct-execution logic in `if __name__ == \"__main__\":` so the file remains safely importable elsewhere.",
            "Iterate over a file object directly (`for line in f:`) rather than `.readlines()` when you don't need every line loaded into memory simultaneously.",
        ],
        pitfalls=[
            "Opening a file without a context manager and forgetting to close it, or closing it in a place that never runs if an earlier line raises an exception.",
            "Relying on the platform's default text encoding instead of specifying `encoding=\"utf-8\"` explicitly, causing different behavior across operating systems.",
            "Confusing relative imports' resolution (based on package structure) with the script's current working directory, leading to a confusing `ImportError: attempted relative import with no known parent package`.",
            "Loading an entire huge file into memory with `.read()` when a line-by-line or chunked approach would use a fraction of the memory.",
        ],
        glossary=[
            dict(term="Context manager", definition="An object (like a file) implementing __enter__/__exit__, used with `with` to guarantee setup and cleanup — see the decorators & context managers lesson."),
            dict(term="Module", definition="Any single .py file, importable by its filename (minus .py) via the import statement."),
            dict(term="Package", definition="A directory containing Python modules, recognized as an importable unit, traditionally marked with an __init__.py file."),
            dict(term="sys.modules", definition="The cache of already-imported modules; re-importing a module elsewhere reuses this cached copy instead of re-running its code."),
            dict(term="__name__ == '__main__'", definition="A guard that's True only when a file is run directly (not imported), used to separate importable logic from run-this-as-a-script logic."),
        ],
        faq=[
            dict(q="Why use pathlib instead of os.path?", a="pathlib gives you an object with methods and operators (like / for joining paths) instead of a collection of separate string-manipulation functions, and it's cross-platform correct by default — most modern Python code prefers it, though os.path is still common in older codebases."),
            dict(q="What actually happens the second time I import a module that's already been imported?", a="Python finds it already in sys.modules and reuses that cached module object instead of re-running the file's top-level code — which is why module-level print statements or side effects only ever run once per program, no matter how many places import that module."),
            dict(q="Why did my relative import fail with 'attempted relative import with no known parent package'?", a="Relative imports require Python to know the importing file's package context, which usually means running it via `python -m package.module` rather than directly executing the file as a script — direct execution doesn't set up that package context."),
        ],
        quiz=[
            dict(
                question="Why is `with open(path) as f:` preferred over manual open()/close()?",
                options=["It's faster to type only", "It guarantees the file is closed even if an exception occurs inside the block", "It's required syntax in Python 3", "It automatically converts text to binary"],
                correct=1,
                explanation="The context manager's __exit__ runs on the way out of the block regardless of whether an exception occurred, guaranteeing cleanup.",
            ),
            dict(
                question="When does `if __name__ == \"__main__\":` block execute?",
                options=["Every time the module is imported", "Only when the file is run directly, not when imported", "Only during testing", "Never, it's a comment convention"],
                correct=1,
                explanation="__name__ is set to '__main__' only for the file that was directly executed; imported modules see their own module name instead.",
            ),
        ],
        prompts=[
            "Why should I use pathlib instead of string concatenation for file paths?",
            "Explain exactly what if __name__ == '__main__' protects against.",
            "Show me how to read a huge file without loading it all into memory at once.",
            "Why did my relative import fail when I ran the file directly?",
        ],
    ),
    dict(
        id="iterators-and-itertools",
        title="Iterators & the itertools Module",
        hook="Every `for` loop in Python is secretly calling `iter()` then `next()` in a loop until it catches a `StopIteration` — understanding that mechanism is what makes itertools click instead of feeling like memorized recipes.",
        explanation=(
            "An iterable is any object you can call `iter()` on to get an iterator; an iterator is an object "
            "with a `__next__` method that returns the next value each time it's called, and raises "
            "`StopIteration` when there's nothing left. A `for` loop is syntactic sugar for calling `iter()` "
            "once and then `next()` repeatedly, catching `StopIteration` to know when to stop — you rarely "
            "need to do this manually, but knowing it's happening explains why generators (which implement "
            "this protocol automatically) slot into `for` loops seamlessly.\n\n"
            "The `itertools` module provides a set of fast, memory-efficient building blocks for working with "
            "iterators, most of which return lazy iterators themselves rather than lists. `itertools.chain(a, "
            "b)` iterates through multiple iterables as if they were one, without concatenating them into a "
            "new list first. `itertools.count(start)` produces an infinite counting sequence. `itertools."
            "islice(iterable, n)` takes the first `n` items from any iterable, including an infinite one, "
            "without needing to know its length in advance.\n\n"
            "`itertools.groupby(iterable, key)` groups consecutive elements sharing a key — critically, it "
            "only groups *consecutive* runs, not all elements sharing a key across the whole sequence, which "
            "is why the input is almost always sorted by the same key first. `itertools.product`, `itertools."
            "permutations`, and `itertools.combinations` generate combinatorial sequences (Cartesian product, "
            "orderings, selections) lazily, which matters enormously once the input size makes the full result "
            "too large to hold in memory at once.\n\n"
            "Built-ins `zip()`, `enumerate()`, `map()`, and `filter()` are themselves lazy iterators in Python "
            "3 (unlike Python 2, where they returned lists), which is why you sometimes need to wrap them in "
            "`list()` to see or index their contents directly, and why they compose efficiently with each "
            "other and with itertools functions without ever materializing an intermediate list."
        ),
        deep_dive=(
            "Custom iterator classes implement both `__iter__` (returning `self`, in the simplest case) and "
            "`__next__` (returning the next value or raising `StopIteration`), which is more verbose than a "
            "generator function but occasionally necessary when you need an object that supports being "
            "iterated over multiple times independently — a generator object is exhausted after one pass, but "
            "a class implementing `__iter__` to return a *new* iterator each time supports being iterated over "
            "repeatedly.\n\n"
            "`itertools.tee(iterable, n)` splits one iterator into several independent ones that can be "
            "consumed separately, which is useful when you need to iterate the same lazy sequence more than "
            "once without converting it to a list first — though it does buffer internally as needed, so it's "
            "not entirely free in memory if the copies fall out of sync in how far they've each advanced.\n\n"
            "Chaining itertools functions together is where they show their real value: `itertools.islice("
            "(x for x in count(1) if is_prime(x)), 10)` lazily generates prime numbers and takes the first 10, "
            "computing only as many candidates as necessary — a pattern that would require either an "
            "artificial upper bound or a completely different algorithm if you tried to express it with eager "
            "list-based code."
        ),
        code=dict(
            lang="python",
            label="chain, islice, and groupby",
            src=(
                "from itertools import chain, islice, groupby\n\n"
                "a = [1, 2, 3]\n"
                "b = [4, 5, 6]\n"
                "print(list(chain(a, b)))              # [1, 2, 3, 4, 5, 6], no new list built until list()\n\n"
                "print(list(islice(range(1_000_000), 5)))   # [0, 1, 2, 3, 4] -- stops early, cheap\n\n"
                "data = sorted([\"apple\", \"avocado\", \"banana\", \"blueberry\"], key=lambda w: w[0])\n"
                "for letter, group in groupby(data, key=lambda w: w[0]):\n"
                "    print(letter, list(group))\n"
                "# a ['apple', 'avocado']\n"
                "# b ['banana', 'blueberry']"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="A custom iterator class, and lazily finding primes",
            src=(
                "class Countdown:\n"
                "    def __init__(self, start):\n"
                "        self.start = start\n\n"
                "    def __iter__(self):\n"
                "        n = self.start\n"
                "        while n > 0:\n"
                "            yield n            # a generator inside __iter__ -- reusable, not exhausted\n"
                "            n -= 1\n\n"
                "cd = Countdown(3)\n"
                "print(list(cd), list(cd))       # [3, 2, 1] [3, 2, 1] -- works twice!\n\n"
                "from itertools import count, islice\n\n"
                "def is_prime(n):\n"
                "    return n > 1 and all(n % i for i in range(2, int(n**0.5) + 1))\n\n"
                "first_10_primes = list(islice((n for n in count(2) if is_prime(n)), 10))\n"
                "print(first_10_primes)          # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]"
            ),
        ),
        example=(
            "A data deduplication script uses `itertools.groupby` on a list of transactions pre-sorted by "
            "customer ID to process each customer's transactions as a batch, without ever building a full "
            "dictionary of customer-to-transactions in memory first."
        ),
        best_practices=[
            "Sort an iterable by the grouping key before using `itertools.groupby` — it only groups consecutive runs, not all matches across the whole sequence.",
            "Reach for `itertools.islice` instead of slicing (`some_generator[:5]`) on a generator, since generators don't support indexing or slicing directly.",
            "Implement `__iter__` to return a fresh generator (or iterator) each time on a custom class you want to support being iterated over multiple times.",
            "Use `itertools.chain` to treat several iterables as one continuous sequence instead of concatenating them into a new list first.",
        ],
        pitfalls=[
            "Calling `itertools.groupby` on unsorted data and being surprised that the 'same' key appears in multiple separate groups because the matching elements weren't consecutive.",
            "Trying to index or slice a generator directly (`my_gen[0]`), which raises a `TypeError` since generators don't support the sequence protocol, only the iterator protocol.",
            "Consuming an `itertools` iterator (like the result of `chain` or `islice`) more than once, expecting it to reset — like generators, most itertools results are single-use.",
        ],
        glossary=[
            dict(term="Iterable", definition="Anything you can call iter() on to get an iterator — lists, strings, dicts, generators, files, and custom classes implementing __iter__."),
            dict(term="Iterator", definition="An object with a __next__ method that produces values one at a time and raises StopIteration when exhausted."),
            dict(term="StopIteration", definition="The exception an iterator raises to signal it has no more values; for loops catch this automatically to know when to stop."),
            dict(term="itertools", definition="A standard library module of fast, memory-efficient, composable functions for working with iterators lazily."),
        ],
        faq=[
            dict(q="What's the practical difference between an iterable and an iterator?", a="An iterable can produce an iterator (via iter()) potentially many times — a list is iterable and you can loop over it repeatedly. An iterator is the one-shot object doing the actual producing of values, exhausted after one full pass."),
            dict(q="Why did groupby split what I expected to be one group into several?", a="groupby only groups consecutive elements with the same key. If the input isn't sorted by that key first, equal keys that aren't adjacent in the sequence form separate groups instead of one."),
            dict(q="Are zip(), map(), and filter() lists or iterators in Python 3?", a="They're lazy iterators, not lists — wrap them in list(...) if you need to see, index, or iterate over the result more than once."),
        ],
        quiz=[
            dict(
                question="What must be true of the input for itertools.groupby to group all matching elements together?",
                options=["It must be a list, not a generator", "It must be sorted by the grouping key first", "It must contain only strings", "Nothing, it automatically groups all matches"],
                correct=1,
                explanation="groupby only groups consecutive runs sharing a key — elements with the same key that aren't adjacent form separate groups unless the data is pre-sorted by that key.",
            ),
            dict(
                question="What does a for loop do under the hood?",
                options=["Directly indexes the iterable with increasing integers", "Calls iter() once, then next() repeatedly until StopIteration", "Converts the iterable to a list first", "Uses recursion internally"],
                correct=1,
                explanation="for loops rely on the iterator protocol: get an iterator with iter(), then repeatedly call next() until StopIteration signals there's nothing left.",
            ),
        ],
        prompts=[
            "Why did itertools.groupby give me more groups than I expected?",
            "Explain the iterator protocol (__iter__ and __next__) with a custom class example.",
            "Show me how to lazily generate an infinite sequence and take just the first N items.",
            "What's the difference between a generator and a class-based iterator, and when would I choose each?",
        ],
    ),
    dict(
        id="typing-and-type-hints",
        title="Type Hints & Static Typing",
        hook="Type hints don't change how your code runs at all — Python still ignores them at runtime — but they turn your editor and a tool like mypy into a second pair of eyes that catches an entire category of bugs before you ever run the code.",
        explanation=(
            "A type hint annotates a variable, parameter, or return value with its expected type: `def "
            "add(a: int, b: int) -> int:` documents that both parameters and the return value should be "
            "integers. Python's interpreter parses and stores these annotations but never enforces or checks "
            "them at runtime — `add(\"a\", \"b\")` runs without error despite violating the hints, because "
            "hints are a documentation and tooling feature, not a runtime contract.\n\n"
            "The `typing` module provides building blocks for more complex hints: `list[int]` (a list of "
            "ints, using the built-in generic syntax available since Python 3.9), `dict[str, float]` (a dict "
            "with string keys and float values), `Optional[str]` (equivalent to `str | None`, meaning the "
            "value could be a string or `None`), and `Union[int, str]` (equivalent to `int | str`, meaning "
            "either type is acceptable).\n\n"
            "A static type checker like `mypy` reads these hints and analyzes your code without running it, "
            "flagging places where the hints don't line up — calling a function with the wrong argument type, "
            "using a value in a way inconsistent with its declared type, or forgetting to handle the `None` "
            "case of an `Optional`. This catches a meaningful class of bugs at development time rather than as "
            "a runtime crash (or worse, silently wrong behavior) in production.\n\n"
            "`TypedDict` lets you describe the expected shape of a dictionary with specific required keys and "
            "value types, which is particularly useful for JSON-like data coming from an API or config file, "
            "where a plain `dict[str, Any]` hint would tell a type checker nothing about which keys are "
            "actually expected to be present."
        ),
        deep_dive=(
            "Generic classes and functions let you write code that works with any type while still preserving "
            "type information — `TypeVar` defines a placeholder type: `def first(items: list[T]) -> T:` says "
            "'this function takes a list of some type T and returns one T', and a type checker can then verify "
            "that `first([1, 2, 3])` returns something treated as an `int`, while `first([\"a\", \"b\"])` "
            "returns something treated as a `str` — the same function, correctly typed for each call site.\n\n"
            "`Protocol` (structural typing) lets you define an interface based purely on what methods/attributes "
            "an object has, rather than what class it explicitly inherits from — `class Sized(Protocol): def "
            "__len__(self) -> int: ...` matches any object with a `__len__` method, regardless of its actual "
            "class hierarchy, which mirrors Python's existing duck-typing philosophy but makes it checkable "
            "statically.\n\n"
            "Type hints have zero runtime cost by default (they're just stored as metadata), but "
            "`from __future__ import annotations` (the default behavior in newer Python versions) treats all "
            "annotations as strings evaluated lazily, avoiding both a small runtime cost and, more importantly, "
            "letting you reference a class in its own methods' hints before the class definition is fully "
            "complete (like a method that returns an instance of its own class)."
        ),
        code=dict(
            lang="python",
            label="Function signatures with type hints",
            src=(
                "def calculate_discount(price: float, percent: float) -> float:\n"
                "    return price * (1 - percent / 100)\n\n"
                "def find_user(user_id: int) -> dict[str, str] | None:\n"
                "    users = {1: {\"name\": \"Amara\"}}\n"
                "    return users.get(user_id)\n\n"
                "from typing import TypedDict\n\n"
                "class UserRecord(TypedDict):\n"
                "    name: str\n"
                "    email: str\n"
                "    age: int\n\n"
                "def create_user(data: UserRecord) -> None:\n"
                "    print(f\"Creating {data['name']}\")   # mypy checks the keys exist and types match"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="A generic function with TypeVar, and a Protocol",
            src=(
                "from typing import TypeVar, Protocol\n\n"
                "T = TypeVar(\"T\")\n\n"
                "def first(items: list[T]) -> T:\n"
                "    return items[0]\n\n"
                "first([1, 2, 3])          # type checker infers T = int, return type int\n"
                "first([\"a\", \"b\"])         # type checker infers T = str, return type str\n\n"
                "class Sized(Protocol):\n"
                "    def __len__(self) -> int: ...\n\n"
                "def describe_size(obj: Sized) -> str:\n"
                "    return f\"Contains {len(obj)} items\"\n\n"
                "describe_size([1, 2, 3])   # list has __len__, satisfies Sized -- no inheritance needed"
            ),
        ),
        example=(
            "A large Flask codebase adds type hints incrementally and runs `mypy` in CI; a refactor that "
            "changes a function to return `Optional[User]` instead of always `User` immediately flags every "
            "call site that forgot to handle the `None` case, before any of those bugs reach production."
        ),
        best_practices=[
            "Add type hints to function signatures first (parameters and return type) — that's where hints deliver the most value for the least effort.",
            "Run a type checker like mypy in CI once a codebase has meaningful type coverage, so hints actually get enforced rather than silently drifting out of date.",
            "Use `Optional[X]` (or `X | None`) explicitly whenever a function can return `None`, rather than letting that possibility go undocumented.",
            "Prefer `Protocol` over requiring a specific base class when you only care that an object supports certain methods, matching Python's duck-typing style.",
        ],
        pitfalls=[
            "Assuming type hints are enforced at runtime and skipping actual input validation for data coming from outside the program (user input, API responses, files).",
            "Adding type hints once and never running a type checker against them, letting the hints silently become inaccurate as the code evolves.",
            "Overusing `Any` as an escape hatch everywhere hints get inconvenient, which defeats the entire purpose of adding them in the first place.",
        ],
        glossary=[
            dict(term="Type hint", definition="An annotation on a variable, parameter, or return value indicating its expected type; not enforced by Python at runtime."),
            dict(term="Static type checker", definition="A tool (like mypy) that analyzes code against its type hints without running it, flagging inconsistencies."),
            dict(term="Optional[X]", definition="Shorthand for X | None, meaning a value is either of type X or None."),
            dict(term="TypeVar / Generic", definition="A placeholder type used to write functions or classes that work with any type while preserving that type's identity through the function's signature."),
            dict(term="Protocol", definition="A structural type definition based on what methods/attributes an object has, matched regardless of its actual class hierarchy."),
        ],
        faq=[
            dict(q="If Python ignores type hints at runtime, what's actually the point?", a="Two things: your editor can give you accurate autocomplete and catch mistakes as you type, and a separate tool like mypy can analyze your whole codebase for type inconsistencies before you ever run it — both catch bugs earlier and cheaper than a runtime crash would."),
            dict(q="Do I need to add type hints to every single variable?", a="No — hints deliver the most value on function signatures (parameters and return types), since that's the interface other code relies on. Hinting every local variable is usually unnecessary; type checkers can often infer those automatically."),
            dict(q="What's the difference between Union[int, str] and int | str?", a="They're equivalent — `X | Y` is newer, more concise syntax (Python 3.10+) for the same thing typing.Union[X, Y] expresses; both mean 'either type is acceptable.'"),
        ],
        quiz=[
            dict(
                question="What happens if you call a function with an argument type that violates its type hint?",
                options=["Python raises a TypeError immediately", "The program still runs; hints aren't enforced at runtime", "It's a SyntaxError", "Python silently converts the argument to the correct type"],
                correct=1,
                explanation="Type hints are purely for tooling and documentation — Python's runtime never checks them, so mismatched calls still execute (and may fail later for unrelated reasons).",
            ),
            dict(
                question="What does Optional[str] mean?",
                options=["The parameter is not required", "The value is either a str or None", "The value must be a string, optionally uppercase", "It has no special meaning"],
                correct=1,
                explanation="Optional[X] is shorthand for X | None — it says the value could be that type, or could be None.",
            ),
        ],
        prompts=[
            "Add type hints to this function and explain what each one communicates.",
            "What's the difference between Protocol and inheriting from an abstract base class?",
            "Why does mypy flag this function even though the code runs fine?",
            "Show me how to type-hint a function that can return either a User object or None.",
        ],
    ),
    dict(
        id="string-formatting-and-regex",
        title="String Formatting & Regular Expressions",
        hook="f-strings replaced nearly every other string-formatting method in modern Python for one simple reason: you write the actual expression inside the string, instead of juggling positional placeholders and a separate argument list.",
        explanation=(
            "An f-string (`f\"Hello, {name}!\"`) evaluates any expression inside `{}` directly and inserts its "
            "string representation — `f\"{price:.2f}\"` formats a float to two decimal places, `f\"{value!r}\"` "
            "uses `repr()` instead of `str()`, and `f\"{name=}\"` (3.8+) is a debugging shortcut that prints "
            "both the expression and its value (`name='Amara'`). Format specifications after the colon control "
            "padding, alignment, decimal places, thousands separators, and more, following a mini-language "
            "shared with the older `.format()` method and `%` formatting.\n\n"
            "The older `str.format()` method (`\"{} scored {}\".format(name, score)`) and the even older `%` "
            "formatting (`\"%s scored %d\" % (name, score)`) still work and appear in existing codebases, but "
            "f-strings are the current idiomatic choice for nearly all new code — they're more concise and, "
            "unlike `%` formatting, don't require matching a format string's placeholders to a separate tuple "
            "of arguments by position.\n\n"
            "Regular expressions (via the `re` module) describe text patterns for searching, matching, and "
            "replacing: `re.search(pattern, text)` finds the first match anywhere in the string, `re.findall"
            "(pattern, text)` returns every non-overlapping match, and `re.sub(pattern, replacement, text)` "
            "replaces matches. Patterns use metacharacters — `\\d` for a digit, `\\w` for a word character, `+` "
            "for one-or-more, `*` for zero-or-more, `?` for optional, `()` for capturing groups.\n\n"
            "Regex is powerful but easy to overuse: for simple substring checks, use `in`; for splitting on a "
            "fixed delimiter, use `.split()`; reach for `re` when the pattern genuinely has variation a plain "
            "string method can't express, like 'a sequence of digits optionally followed by a decimal point "
            "and more digits.'"
        ),
        deep_dive=(
            "Compiling a regex pattern once with `re.compile(pattern)` and reusing the resulting pattern "
            "object across many calls is meaningfully faster than passing the raw string pattern to `re."
            "search`/`re.findall` repeatedly, because Python has to re-parse and re-compile the pattern "
            "internally on every call otherwise (though it does cache recently used patterns, so this mostly "
            "matters in genuinely hot loops).\n\n"
            "Named capture groups (`(?P<year>\\d{4})-(?P<month>\\d{2})`) let you extract matched pieces by "
            "name instead of positional index (`match.group(\"year\")` instead of `match.group(1)`), which "
            "makes complex patterns with several groups dramatically more maintainable — the pattern documents "
            "its own structure.\n\n"
            "Raw strings (`r\"\\d+\"`) are almost always used for regex patterns because backslashes have "
            "special meaning in both regular Python strings (`\\n` is a newline) and regex syntax (`\\d` is a "
            "digit) — a raw string tells Python not to interpret the backslash as an escape sequence, letting "
            "the regex engine see the literal `\\d` it expects, rather than Python trying (and usually failing) "
            "to interpret `\\d` as some other escape sequence first."
        ),
        code=dict(
            lang="python",
            label="f-string formatting options",
            src=(
                "name, score, price = \"Amara\", 94.567, 19.9\n\n"
                "print(f\"{name} scored {score:.1f}%\")        # Amara scored 94.6%\n"
                "print(f\"${price:,.2f}\")                     # $19.90\n"
                "print(f\"{name:>10}\")                        # '     Amara' -- right-aligned, width 10\n"
                "print(f\"{name=}\")                           # name='Amara' -- debug shortcut\n"
                "print(f\"{'yes' if score > 90 else 'no'}\")   # any expression works inside {}"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Named capture groups and compiled patterns",
            src=(
                "import re\n\n"
                "log_pattern = re.compile(\n"
                "    r\"(?P<date>\\d{4}-\\d{2}-\\d{2}) \"\n"
                "    r\"(?P<level>ERROR|WARN|INFO) \"\n"
                "    r\"(?P<message>.+)\"\n"
                ")\n\n"
                "line = \"2026-07-19 ERROR Database connection timed out\"\n"
                "match = log_pattern.match(line)\n"
                "if match:\n"
                "    print(match.group(\"date\"))       # 2026-07-19\n"
                "    print(match.group(\"level\"))      # ERROR\n"
                "    print(match.group(\"message\"))    # Database connection timed out"
            ),
        ),
        example=(
            "A log-parsing script compiles one regex pattern with named groups for date, log level, and "
            "message, then runs it against millions of log lines — extracting structured fields from "
            "unstructured text far more reliably than manual string slicing that assumes fixed column "
            "positions."
        ),
        best_practices=[
            "Default to f-strings for new code; reserve `.format()` mainly for cases building a format string dynamically before applying it.",
            "Use raw strings (`r\"...\"`) for every regex pattern, to avoid backslash escape-sequence conflicts between Python and regex syntax.",
            "Compile a regex with `re.compile()` when the same pattern is used repeatedly, especially inside a loop.",
            "Use named capture groups for patterns with more than one or two groups, so the code documents what each captured piece represents.",
            "Reach for plain string methods (`in`, `.split()`, `.startswith()`) before regex whenever the pattern is simple enough not to need it.",
        ],
        pitfalls=[
            "Forgetting the `r` prefix on a regex pattern containing backslashes, causing Python to interpret them as string escape sequences before the regex engine ever sees the pattern.",
            "Reaching for regex to validate something with a genuinely well-defined format (like an email address) where a purpose-built library handles more edge cases correctly than a hand-rolled pattern.",
            "Writing an overly greedy pattern (`.*` instead of a more specific `[^,]*`) that matches far more text than intended.",
            "Using `%` formatting with mismatched argument counts or types, which raises a runtime error only when that line actually executes, not at write time.",
        ],
        glossary=[
            dict(term="f-string", definition="A string literal prefixed with f that evaluates expressions inside {} directly and inserts their string representation."),
            dict(term="Format specification", definition="The part after a colon inside an f-string's {}, controlling decimal places, alignment, padding, and similar formatting details."),
            dict(term="Capture group", definition="A parenthesized section of a regex pattern whose match can be extracted separately; named groups use (?P<name>...) syntax."),
            dict(term="Raw string", definition="A string literal prefixed with r that disables backslash escape sequence interpretation, almost always used for regex patterns."),
        ],
        faq=[
            dict(q="Why do regex patterns almost always use r-strings?", a="Both Python strings and regex syntax use backslashes for special meaning (\\n vs \\d, for example). A raw string tells Python to pass backslashes through literally, so the regex engine receives exactly the pattern you wrote instead of Python trying to interpret it first."),
            dict(q="When should I use regex instead of just .split() or .replace()?", a="When the pattern has genuine variation that a fixed string method can't express — matching 'any sequence of digits', 'an optional decimal part', or 'one of several possible words' are jobs for regex; splitting on a single, fixed, known delimiter is not."),
            dict(q="What's the difference between re.match and re.search?", a="re.match only checks for a match at the very start of the string; re.search checks the entire string for a match anywhere within it."),
        ],
        quiz=[
            dict(
                question="What does f\"{price:.2f}\" do?",
                options=["Converts price to a string with 2 characters", "Formats price as a float with 2 decimal places", "Rounds price to the nearest 2", "Raises an error if price isn't already a float"],
                correct=1,
                explanation="The :.2f format spec formats a numeric value as a fixed-point float with exactly 2 digits after the decimal point.",
            ),
            dict(
                question="Why use re.compile() for a pattern used inside a loop running thousands of times?",
                options=["It's required syntax", "It avoids re-parsing the pattern string on every single call", "It makes the pattern case-insensitive automatically", "compile() is the only way to use named groups"],
                correct=1,
                explanation="Compiling once and reusing the pattern object avoids the overhead of re-parsing the same pattern string on every iteration.",
            ),
        ],
        prompts=[
            "Write a regex with named groups to parse this log line format.",
            "Convert this old-style % formatting to an f-string.",
            "Why isn't my regex matching, even though the pattern looks right to me?",
            "When should I reach for regex instead of a simple string method?",
        ],
    ),
    dict(
        id="concurrency-basics",
        title="Concurrency: Threading, Multiprocessing & asyncio",
        hook="Python has three completely different ways to run things 'at the same time', and picking the wrong one for your problem either does nothing for performance or actively makes it worse — the GIL is the reason why.",
        explanation=(
            "CPython has a Global Interpreter Lock (GIL) — a single lock ensuring only one thread executes "
            "Python bytecode at any given instant, even on a multi-core machine. This means Python threads "
            "don't give you true CPU parallelism for pure Python computation, which surprises people coming "
            "from languages without this restriction. Threads still have a real, important use case though: "
            "I/O-bound work (network requests, file reads, database queries), where a thread waiting on I/O "
            "releases the GIL, letting other threads run during that wait.\n\n"
            "`multiprocessing` sidesteps the GIL entirely by running separate Python processes, each with its "
            "own interpreter and memory space, communicating through message passing or shared memory rather "
            "than shared variables. This gives genuine CPU parallelism across cores, at the cost of higher "
            "memory usage and slower startup per worker compared to threads, and the requirement that data "
            "passed between processes be picklable (serializable).\n\n"
            "`asyncio` provides single-threaded concurrency through cooperative multitasking: an event loop "
            "runs many coroutines that voluntarily yield control (`await`) at points where they'd otherwise be "
            "waiting on I/O, letting the event loop run other coroutines during that wait. This achieves high "
            "concurrency for I/O-bound work without the overhead of threads or processes, but requires the "
            "entire call chain to be written with `async`/`await` — a single blocking call inside a coroutine "
            "stalls the whole event loop.\n\n"
            "The practical decision rule: CPU-bound work (heavy computation) needs `multiprocessing` to "
            "actually use multiple cores. I/O-bound work with a moderate number of concurrent operations "
            "(dozens) works well with `threading`. I/O-bound work needing very high concurrency (thousands of "
            "simultaneous connections, like a web server) is where `asyncio` shines."
        ),
        deep_dive=(
            "The GIL exists because CPython's memory management (reference counting) isn't thread-safe without "
            "it — removing it would require a fundamentally different, more complex memory management scheme, "
            "which is exactly what ongoing 'free-threaded Python' (PEP 703) work is attempting, though it "
            "remains experimental and not yet the default in most deployed Python versions as of this writing.\n\n"
            "`asyncio.gather(*coroutines)` runs multiple coroutines concurrently and waits for all of them to "
            "complete, which is the async equivalent of firing off several I/O operations at once instead of "
            "awaiting them one at a time sequentially — the difference between fetching 10 URLs concurrently "
            "in roughly the time of the slowest one, versus sequentially in the sum of all their times.\n\n"
            "`concurrent.futures` provides a higher-level, unified interface over both threads (`ThreadPoolExecutor`) "
            "and processes (`ProcessPoolExecutor`) with the same `.submit()`/`.map()` API, which is often the "
            "easiest entry point for straightforward parallelism without directly managing `threading.Thread` "
            "or `multiprocessing.Process` objects and their lifecycle."
        ),
        code=dict(
            lang="python",
            label="ThreadPoolExecutor for I/O-bound work",
            src=(
                "from concurrent.futures import ThreadPoolExecutor\n"
                "import requests\n\n"
                "urls = [\"https://api.example.com/1\", \"https://api.example.com/2\", \"https://api.example.com/3\"]\n\n"
                "def fetch(url):\n"
                "    return requests.get(url, timeout=10).status_code\n\n"
                "with ThreadPoolExecutor(max_workers=5) as pool:\n"
                "    results = list(pool.map(fetch, urls))   # runs concurrently, I/O-bound\n"
                "print(results)"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="asyncio with gather for concurrent I/O",
            src=(
                "import asyncio\n"
                "import aiohttp\n\n"
                "async def fetch(session, url):\n"
                "    async with session.get(url) as response:\n"
                "        return response.status\n\n"
                "async def main():\n"
                "    urls = [\"https://api.example.com/1\", \"https://api.example.com/2\"]\n"
                "    async with aiohttp.ClientSession() as session:\n"
                "        results = await asyncio.gather(*[fetch(session, u) for u in urls])\n"
                "    return results\n\n"
                "results = asyncio.run(main())   # concurrent, single-threaded, event-loop driven"
            ),
        ),
        example=(
            "A script downloading 500 web pages runs in a fraction of the time using `ThreadPoolExecutor` or "
            "`asyncio` compared to a plain sequential loop, because nearly all the time is spent waiting on "
            "network I/O — but a CPU-heavy image-processing script applied to 500 images sees no speedup at "
            "all from threading, and needs `multiprocessing` to actually use multiple CPU cores."
        ),
        best_practices=[
            "Match the concurrency tool to the bottleneck: multiprocessing for CPU-bound work, threading or asyncio for I/O-bound work.",
            "Use `concurrent.futures` (ThreadPoolExecutor/ProcessPoolExecutor) as the default entry point before reaching for lower-level threading or multiprocessing APIs directly.",
            "In asyncio code, use `asyncio.gather` to run independent I/O operations concurrently rather than awaiting them one at a time in a loop.",
            "Never mix blocking, synchronous I/O calls inside an async function — it stalls the entire event loop for every other coroutine.",
        ],
        pitfalls=[
            "Using `threading` for CPU-bound work and being confused why it's no faster (sometimes slower, due to overhead) than a single-threaded loop — the GIL prevents true parallel computation across threads.",
            "Calling a blocking function (like `time.sleep` or a synchronous `requests.get`) inside an `async def` coroutine, which freezes the entire event loop for the duration of that call.",
            "Passing non-picklable objects (like open file handles or database connections) between processes with `multiprocessing`, which raises a serialization error.",
        ],
        glossary=[
            dict(term="GIL (Global Interpreter Lock)", definition="A CPython-specific lock ensuring only one thread executes Python bytecode at a time, limiting threads' usefulness for CPU-bound parallelism."),
            dict(term="I/O-bound", definition="A task spending most of its time waiting on external operations (network, disk, database) rather than actively computing."),
            dict(term="CPU-bound", definition="A task spending most of its time on active computation, limited by processor speed rather than waiting on external operations."),
            dict(term="Event loop", definition="The core of asyncio, which runs coroutines and switches between them at await points, achieving concurrency on a single thread."),
            dict(term="Coroutine", definition="A function defined with async def, which can be paused at await points and resumed later by the event loop."),
        ],
        faq=[
            dict(q="If Python has a GIL, is multithreading ever actually useful?", a="Yes, for I/O-bound work — a thread waiting on a network response or disk read releases the GIL, letting other threads run during that wait. It just doesn't give you parallel CPU computation for pure Python code."),
            dict(q="Why does asyncio need every function in the call chain to be async?", a="Because a coroutine only yields control at an await point; if any function in the chain does a blocking call without awaiting, it holds onto the single thread and stalls the entire event loop for every other coroutine waiting to run."),
            dict(q="Why can't I just pass a database connection object between processes in multiprocessing?", a="multiprocessing communicates between processes by pickling (serializing) objects, and many objects — open file handles, network connections, database connections — hold OS-level resources that can't be meaningfully serialized and recreated in another process."),
        ],
        quiz=[
            dict(
                question="Why doesn't Python threading speed up a CPU-bound computation across multiple cores?",
                options=["Threading is broken in Python", "The GIL ensures only one thread runs Python bytecode at a time", "CPU-bound tasks can't use threads at all", "Threads are slower than a single loop always"],
                correct=1,
                explanation="The GIL serializes execution of Python bytecode across threads, so CPU-bound work sees no parallel speedup from threading alone — multiprocessing is needed for that.",
            ),
            dict(
                question="What's the danger of calling a blocking (synchronous) function inside an async coroutine?",
                options=["It raises a SyntaxError", "It stalls the entire event loop, blocking every other coroutine", "Nothing, async functions handle it automatically", "It only slows down that one coroutine"],
                correct=1,
                explanation="Since asyncio is single-threaded, a blocking call holds the only thread hostage, preventing the event loop from running any other coroutine until it returns.",
            ),
        ],
        prompts=[
            "Should I use threading, multiprocessing, or asyncio for this specific task?",
            "Explain why the GIL exists and what removing it would require.",
            "Convert this sequential loop of API calls into concurrent requests with asyncio.",
            "Why did adding more threads not speed up my CPU-heavy computation at all?",
        ],
    ),
    dict(
        id="dataclasses-and-namedtuples",
        title="dataclasses & NamedTuple",
        hook="A class that's mostly just a bundle of fields with an __init__, __repr__, and __eq__ is one of the most common patterns in Python — and `@dataclass` writes all that boilerplate for you from a handful of type-annotated lines.",
        explanation=(
            "`@dataclass` is a class decorator that automatically generates `__init__`, `__repr__`, and "
            "`__eq__` based on the class's type-annotated fields, eliminating the repetitive boilerplate of "
            "writing `self.x = x` for every field by hand. `@dataclass class Point: x: float; y: float` gives "
            "you a working `Point(1.0, 2.0)` constructor, a readable `repr()`, and value-based equality "
            "(`Point(1,2) == Point(1,2)` is `True`) with just two lines describing the fields.\n\n"
            "Fields can have default values (`z: float = 0.0`), and `field(default_factory=list)` handles "
            "mutable defaults correctly — dataclasses specifically forbid a bare mutable default like `items: "
            "list = []` at the class level (raising an error at class definition time) precisely because of "
            "the shared-mutable-default bug that plagues function default arguments; `default_factory` calls a "
            "function to produce a fresh object for every new instance instead.\n\n"
            "`NamedTuple` (from `typing`) is a lighter-weight alternative for simple, immutable records: "
            "`class Point(NamedTuple): x: float; y: float` behaves like a regular tuple (supports unpacking, "
            "indexing, iteration) but with named field access (`point.x`) on top, and is genuinely immutable — "
            "unlike a dataclass's fields, which are mutable by default unless you pass `frozen=True`.\n\n"
            "Both are dramatically less verbose than a hand-written equivalent class, and both integrate "
            "cleanly with type hints, making them the idiomatic choice for 'plain data' objects — configuration "
            "objects, API response records, coordinates, anything that's primarily a structured bundle of "
            "values rather than an object with significant behavior of its own."
        ),
        deep_dive=(
            "`@dataclass(frozen=True)` makes instances immutable after creation — attempting to set an "
            "attribute after `__init__` raises an error — which also makes the dataclass hashable by default "
            "(since Python can safely assume a frozen object's hash won't change), letting frozen dataclass "
            "instances be used as dict keys or set members, unlike regular mutable dataclasses.\n\n"
            "`@dataclass(order=True)` additionally generates comparison methods (`__lt__`, `__le__`, etc.) "
            "based on the fields in the order they're declared, letting instances be sorted directly with "
            "`sorted()` — comparing tuples of field values in declaration order, the same way tuples compare "
            "element by element.\n\n"
            "For deeper validation or computed fields, `__post_init__` runs automatically right after the "
            "generated `__init__` completes, letting you add custom logic (validating a range, computing a "
            "derived field from the others) without having to hand-write the entire `__init__` yourself — you "
            "keep the automatic boilerplate generation and layer custom behavior on top of it."
        ),
        code=dict(
            lang="python",
            label="A basic dataclass vs. the hand-written equivalent",
            src=(
                "from dataclasses import dataclass, field\n\n"
                "@dataclass\n"
                "class Product:\n"
                "    name: str\n"
                "    price: float\n"
                "    tags: list[str] = field(default_factory=list)   # safe mutable default\n\n"
                "p1 = Product(\"Keyboard\", 49.99)\n"
                "p2 = Product(\"Keyboard\", 49.99)\n"
                "print(p1)                 # Product(name='Keyboard', price=49.99, tags=[])\n"
                "print(p1 == p2)           # True -- value equality, generated automatically"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="frozen dataclass, ordering, and __post_init__ validation",
            src=(
                "from dataclasses import dataclass\n\n"
                "@dataclass(frozen=True, order=True)\n"
                "class Version:\n"
                "    major: int\n"
                "    minor: int\n"
                "    patch: int\n\n"
                "    def __post_init__(self):\n"
                "        if self.major < 0:\n"
                "            raise ValueError(\"major version can't be negative\")\n\n"
                "versions = [Version(1, 2, 0), Version(1, 0, 5), Version(2, 0, 0)]\n"
                "print(sorted(versions))   # sorted by (major, minor, patch) tuple order\n\n"
                "v = Version(1, 0, 0)\n"
                "# v.major = 2             # raises: cannot assign to field (frozen)\n"
                "print(hash(v))            # frozen dataclasses are hashable"
            ),
        ),
        example=(
            "An API client library defines its response models as frozen dataclasses — once a `Response` "
            "object is constructed from the JSON payload, nothing downstream in the codebase can accidentally "
            "mutate it, which eliminates an entire category of 'who changed this object and when' bugs in a "
            "larger codebase."
        ),
        best_practices=[
            "Use `@dataclass` for any class that's primarily a bundle of related fields, instead of hand-writing `__init__`/`__repr__`/`__eq__`.",
            "Use `field(default_factory=...)` for any mutable default (list, dict, set) — a bare mutable default at the class level raises an error specifically to prevent the shared-default bug.",
            "Reach for `frozen=True` on any dataclass representing a value that shouldn't change after creation, gaining both safety and hashability.",
            "Use `NamedTuple` instead of `@dataclass` when you specifically want tuple-like behavior (unpacking, indexing) alongside named fields.",
        ],
        pitfalls=[
            "Trying to set a mutable default directly (`items: list = []`) on a dataclass field, which raises a `ValueError` at class definition time rather than silently causing the shared-default bug.",
            "Forgetting that regular (non-frozen) dataclasses are mutable and not hashable by default, then being surprised they can't be used as dict keys.",
            "Reaching for a full class with manually written boilerplate when a dataclass or NamedTuple would express the same 'bundle of fields' intent in far fewer lines.",
        ],
        glossary=[
            dict(term="@dataclass", definition="A class decorator that auto-generates __init__, __repr__, and __eq__ from type-annotated class fields."),
            dict(term="field(default_factory=...)", definition="A dataclasses helper that produces a fresh mutable default value for each new instance, avoiding the shared-mutable-default bug."),
            dict(term="frozen dataclass", definition="A dataclass created with frozen=True, making its fields immutable after construction and the instance hashable."),
            dict(term="NamedTuple", definition="A typing-module class that behaves like an immutable tuple with named field access, lighter-weight than a dataclass."),
        ],
        faq=[
            dict(q="Why can't I just write `items: list = []` as a dataclass field default?", a="dataclasses specifically detect this pattern and raise an error, because a bare mutable default would be shared across every instance — the same bug as mutable default function arguments. Use field(default_factory=list) instead, which creates a fresh list per instance."),
            dict(q="Should I use a dataclass or a NamedTuple for a simple coordinate pair?", a="Either works; NamedTuple is slightly lighter-weight and gives you tuple behavior (unpacking, indexing) for free, while a dataclass is more flexible if you expect to add methods, mutability, or more complex validation later."),
            dict(q="Are dataclass instances hashable by default?", a="No — regular dataclasses are mutable by default and therefore not hashable. Passing frozen=True makes them immutable and automatically hashable, so they can be used as dict keys or set members."),
        ],
        quiz=[
            dict(
                question="What does @dataclass automatically generate for you?",
                options=["Only __init__", "__init__, __repr__, and __eq__ based on the fields", "A full REST API", "Database migrations"],
                correct=1,
                explanation="@dataclass generates the constructor, a readable string representation, and value-based equality automatically from the annotated fields.",
            ),
            dict(
                question="Why does `items: list = []` raise an error in a dataclass but not in a plain function default?",
                options=["It doesn't raise an error in either case", "dataclasses explicitly detect and forbid mutable defaults to prevent the shared-default bug", "Lists aren't allowed as dataclass fields at all", "It's a typo, not related to mutability"],
                correct=1,
                explanation="dataclasses proactively raise a ValueError for bare mutable defaults, requiring field(default_factory=list) instead, precisely because the bug is so common and easy to prevent structurally.",
            ),
        ],
        prompts=[
            "Convert this hand-written class into a dataclass.",
            "When should I use NamedTuple instead of @dataclass?",
            "Explain why frozen=True also makes a dataclass hashable.",
            "Show me how to add custom validation to a dataclass with __post_init__.",
        ],
    ),
    dict(
        id="modules-packaging-venvs",
        title="Packaging, pip & Virtual Environments",
        hook="Installing a package globally on your system feels convenient right up until two projects need two different, incompatible versions of the same library — which is exactly the problem virtual environments exist to solve.",
        explanation=(
            "A virtual environment is an isolated Python installation with its own `site-packages` directory, "
            "letting each project have its own independent set of installed package versions without "
            "conflicting with other projects or the system Python. `python -m venv venv` creates one; "
            "activating it (`source venv/bin/activate` on macOS/Linux, `venv\\Scripts\\activate` on Windows) "
            "changes your shell's `python` and `pip` to point at that isolated environment until you "
            "deactivate it.\n\n"
            "`pip` is Python's package installer, pulling packages from PyPI (the Python Package Index) by "
            "default. `pip install package_name` installs the latest compatible version; `pip install "
            "package_name==1.2.3` pins an exact version. `requirements.txt` lists a project's dependencies "
            "(usually with pinned versions) so `pip install -r requirements.txt` reproduces the same "
            "environment on another machine or in CI.\n\n"
            "A `pyproject.toml` file is the modern, standardized way to declare a project's metadata and "
            "dependencies, gradually replacing the older combination of `setup.py` and `requirements.txt` for "
            "publishable packages — tools like `poetry`, `hatch`, and modern `pip` itself all read from it.\n\n"
            "Publishing your own package to PyPI involves structuring the project with a `pyproject.toml`, "
            "building a distribution (`python -m build`), and uploading it (`twine upload dist/*`) — after "
            "which anyone can `pip install your-package-name`."
        ),
        deep_dive=(
            "Dependency resolution is where package management gets genuinely hard: if package A requires "
            "`requests>=2.0` and package B requires `requests<2.0`, pip has to find a version satisfying both "
            "constraints or fail loudly — this is why pinning overly broad or overly narrow version ranges in "
            "your own package's dependencies can cause real friction for anyone trying to use it alongside "
            "other packages.\n\n"
            "Lock files (like `poetry.lock` or `requirements-lock.txt` generated by `pip-compile`) go a step "
            "further than `requirements.txt` by recording the *exact* resolved version of every dependency "
            "(including transitive dependencies — the dependencies of your dependencies), guaranteeing a truly "
            "reproducible environment rather than one that could shift slightly as sub-dependencies release "
            "new versions.\n\n"
            "`pip freeze > requirements.txt` is a common but imperfect way to generate a requirements file — it "
            "captures every package installed in the environment, including ones you didn't directly choose "
            "(transitive dependencies), which makes the file harder to read and maintain than one written by "
            "hand listing only your project's actual direct dependencies with sensible version ranges."
        ),
        code=dict(
            lang="bash",
            label="The standard virtual environment workflow",
            src=(
                "python -m venv venv\n"
                "source venv/bin/activate          # Windows: venv\\Scripts\\activate\n\n"
                "pip install flask requests\n"
                "pip freeze > requirements.txt      # snapshot exact installed versions\n\n"
                "# on another machine, or in CI:\n"
                "python -m venv venv\n"
                "source venv/bin/activate\n"
                "pip install -r requirements.txt    # reproduce the same environment\n\n"
                "deactivate                          # leave the virtual environment"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="A minimal pyproject.toml for a publishable package",
            src=(
                "[project]\n"
                "name = \"finese-utils\"\n"
                "version = \"0.1.0\"\n"
                "description = \"Small utilities used across FINESE SCHOOL examples\"\n"
                "dependencies = [\n"
                "    \"requests>=2.31,<3.0\",\n"
                "]\n\n"
                "[build-system]\n"
                "requires = [\"setuptools>=68\"]\n"
                "build-backend = \"setuptools.build_meta\""
            ),
        ),
        example=(
            "A team with one project pinned to an older Flask version and another using the latest Flask "
            "avoids any conflict entirely because each project has its own virtual environment — without "
            "isolation, installing the newer Flask globally would silently break the older project the moment "
            "someone ran it."
        ),
        best_practices=[
            "Create a fresh virtual environment per project, never installing project dependencies into the system-wide Python.",
            "Commit `requirements.txt` (or a lock file) to version control so the exact environment is reproducible by teammates and CI.",
            "Pin dependency versions for applications (things you deploy) more strictly than for libraries (things others install alongside their own dependencies).",
            "Regenerate and review `requirements.txt` periodically rather than letting it silently drift out of sync with what's actually imported in the code.",
        ],
        pitfalls=[
            "Installing packages globally without a virtual environment, leading to version conflicts between unrelated projects sharing one Python installation.",
            "Committing a virtual environment folder itself to version control instead of just the requirements file — it's large, platform-specific, and unnecessary to share.",
            "Using `pip freeze` blindly for a library's `requirements.txt`, which locks the library's users into exact versions of dependencies they might need looser constraints on.",
        ],
        glossary=[
            dict(term="Virtual environment", definition="An isolated Python installation with its own installed packages, keeping project dependencies separate from the system Python and other projects."),
            dict(term="PyPI", definition="The Python Package Index, the default public repository pip installs packages from."),
            dict(term="requirements.txt", definition="A plain text file listing a project's dependencies, typically with version constraints, used to reproduce an environment."),
            dict(term="Lock file", definition="A file recording the exact resolved version of every dependency (including transitive ones), guaranteeing a fully reproducible install."),
            dict(term="Transitive dependency", definition="A dependency of one of your dependencies, not something you installed directly yourself."),
        ],
        faq=[
            dict(q="Do I need a virtual environment for every small script I write?", a="For quick throwaway scripts, not strictly — but for anything you'll return to, share, or deploy, yes: it costs almost nothing to set up and prevents an entire category of 'works on my machine' problems."),
            dict(q="What's the difference between requirements.txt and pyproject.toml?", a="requirements.txt is a simple list of dependencies for pip to install, commonly used for applications. pyproject.toml is a more complete, standardized project descriptor (metadata, build configuration, dependencies) increasingly used for both applications and especially publishable packages."),
            dict(q="Why shouldn't I just install everything globally to save time?", a="It works fine until you have two projects needing incompatible versions of the same package, or until you can't reproduce a colleague's exact environment — isolation avoids both problems from the start rather than debugging them later."),
        ],
        quiz=[
            dict(
                question="What problem do virtual environments primarily solve?",
                options=["Making Python run faster", "Isolating each project's dependencies from other projects and the system Python", "Automatically writing your code", "Encrypting your source code"],
                correct=1,
                explanation="Virtual environments give each project its own independent set of installed package versions, preventing conflicts between projects.",
            ),
        ],
        prompts=[
            "Walk me through setting up a virtual environment for a new Flask project.",
            "What's the difference between requirements.txt and a lock file?",
            "Why did installing a new package break an unrelated project on my machine?",
            "Help me write a pyproject.toml for a small package I want to publish.",
        ],
    ),
    dict(
        id="functional-tools",
        title="Functional Programming Tools: map, filter, functools",
        hook="Python isn't a purely functional language, but map, filter, and the functools module give you real functional-style tools when they genuinely make code clearer than the imperative alternative.",
        explanation=(
            "`map(function, iterable)` applies a function to every item of an iterable lazily, returning an "
            "iterator of results — `map(str.upper, words)` is a lazy, functional alternative to a list "
            "comprehension doing the same transformation, though in modern Python a comprehension "
            "(`[w.upper() for w in words]`) is often considered more readable for simple cases, with `map` "
            "still valuable when you already have a named function to apply. `filter(predicate, iterable)` "
            "keeps only items where the predicate function returns truthy, also lazily.\n\n"
            "`functools.reduce(function, iterable, initial)` repeatedly applies a two-argument function, "
            "accumulating a single result — `reduce(lambda acc, x: acc + x, numbers, 0)` sums a list "
            "(though `sum()` is the better tool for that specific case; `reduce` shines for accumulations "
            "that don't have a dedicated built-in, like finding the item with the maximum value under some "
            "custom rule, or composing a chain of transformations).\n\n"
            "`functools.partial(function, *fixed_args)` creates a new function with some arguments already "
            "'baked in' — `partial(requests.get, timeout=10)` produces a `get`-like function that always uses "
            "a 10-second timeout, useful for adapting a general function to a more specific, reusable "
            "callable without writing a full wrapper function.\n\n"
            "`functools.lru_cache` (or the newer `functools.cache`) memoizes a function's results, "
            "automatically caching return values by argument so repeated calls with the same arguments skip "
            "re-computation entirely — a one-line decorator that can turn an expensive recursive function "
            "(like naive Fibonacci) from exponential to linear time."
        ),
        deep_dive=(
            "Lambda expressions (`lambda x: x * 2`) create small anonymous functions inline, most commonly "
            "used as the `key` argument to `sorted()`, `max()`, `min()`, or as the function argument to `map`/"
            "`filter` for logic too small to justify a separate named `def`. A lambda is restricted to a "
            "single expression (no statements, no multiple lines), which is a deliberate limitation keeping "
            "them genuinely small — anything more complex should be a regular named function for readability.\n\n"
            "`functools.lru_cache`'s cache is keyed by the function's arguments, which must therefore be "
            "hashable — calling a cached function with a list argument raises a `TypeError`, since lists can't "
            "be dict keys. The cache also has a `maxsize` parameter (default 128) controlling how many distinct "
            "argument combinations it remembers before evicting the least recently used entry, preventing "
            "unbounded memory growth for functions called with many different arguments over a long-running "
            "program.\n\n"
            "Function composition — building a new function by chaining several together — isn't built into "
            "Python directly the way it is in some functional languages, but is easy to express manually: `def "
            "compose(*funcs): return lambda x: functools.reduce(lambda acc, f: f(acc), funcs, x)` chains "
            "functions right-to-left, a small but genuinely useful pattern when building data-processing "
            "pipelines out of small, single-purpose functions."
        ),
        code=dict(
            lang="python",
            label="map, filter, and reduce",
            src=(
                "from functools import reduce\n\n"
                "words = [\"hello\", \"world\", \"python\"]\n"
                "print(list(map(str.upper, words)))              # ['HELLO', 'WORLD', 'PYTHON']\n\n"
                "numbers = [1, 2, 3, 4, 5, 6]\n"
                "evens = list(filter(lambda n: n % 2 == 0, numbers))\n"
                "print(evens)                                     # [2, 4, 6]\n\n"
                "product = reduce(lambda acc, n: acc * n, numbers, 1)\n"
                "print(product)                                    # 720"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="lru_cache turning exponential recursion into linear time",
            src=(
                "from functools import lru_cache, partial\n\n"
                "@lru_cache(maxsize=None)\n"
                "def fib(n):\n"
                "    if n < 2:\n"
                "        return n\n"
                "    return fib(n - 1) + fib(n - 2)          # without caching: exponential time\n\n"
                "print(fib(35))                                # instant, thanks to memoization\n\n"
                "get_with_timeout = partial(requests.get, timeout=10)\n"
                "response = get_with_timeout(\"https://api.example.com\")   # timeout already baked in"
            ),
        ),
        example=(
            "An API client wraps `requests.get` with `functools.partial` to bake in a shared timeout and base "
            "headers across every call site, and wraps an expensive currency-conversion lookup with "
            "`lru_cache` so repeated conversions between the same currency pair within a session skip the "
            "external API call entirely."
        ),
        best_practices=[
            "Use a list/dict/set comprehension over `map`/`filter` for simple transformations — it's generally considered more readable in modern Python, reserving map/filter for when you already have a named function to apply.",
            "Add `@lru_cache` to pure functions (same input always produces same output, no side effects) that are called repeatedly with a limited set of distinct arguments.",
            "Use `functools.partial` to adapt a general-purpose function into a specialized, reusable one instead of writing a small wrapper function by hand.",
            "Keep lambdas to genuinely trivial one-line logic; anything requiring a comment to explain should be a named function instead.",
        ],
        pitfalls=[
            "Applying `@lru_cache` to a function with side effects or one whose result can change for the same arguments (like a function reading live external state) — the cache will return a stale result.",
            "Calling an `lru_cache`-decorated function with unhashable arguments (like a list), which raises a `TypeError`.",
            "Overusing `reduce` for operations that already have a clear, more readable built-in (`sum`, `max`, `min`, `any`, `all`).",
        ],
        glossary=[
            dict(term="Lambda", definition="An anonymous, single-expression function created inline with the lambda keyword, commonly used for short key/sort functions."),
            dict(term="Memoization", definition="Caching a function's results by its arguments so repeated calls with the same input skip recomputation."),
            dict(term="Pure function", definition="A function whose output depends only on its inputs, with no side effects — the ideal candidate for caching with lru_cache."),
            dict(term="functools.partial", definition="Creates a new callable with some arguments of an existing function pre-filled ('frozen in')."),
        ],
        faq=[
            dict(q="Should I use map/filter or a list comprehension?", a="For simple cases, most Python style guides and developers prefer comprehensions for readability. map/filter still earn their place when you're applying an existing named function without needing a lambda wrapper."),
            dict(q="Why did adding lru_cache to my function cause a TypeError?", a="lru_cache needs to hash the function's arguments to use them as a cache key. If you call it with an unhashable argument like a list or dict, hashing fails — convert to a tuple or frozenset first, or don't cache that function."),
            dict(q="Is lru_cache safe to use on a function that reads from a database?", a="Only if the underlying data won't change during the program's run in a way that should be reflected — otherwise the cache will happily return stale results forever (or until the process restarts), since it has no way to know the underlying data changed."),
        ],
        quiz=[
            dict(
                question="What does functools.lru_cache do?",
                options=["Deletes old function definitions", "Caches a function's return values keyed by its arguments", "Limits how many times a function can be called", "Converts a function to run in a separate thread"],
                correct=1,
                explanation="lru_cache memoizes results: repeated calls with the same arguments return the cached result instead of recomputing.",
            ),
        ],
        prompts=[
            "When should I use lru_cache, and what functions are unsafe to cache this way?",
            "Convert this reduce() call into a more readable built-in function if one exists.",
            "Show me how functools.partial simplifies repeated calls with the same fixed argument.",
            "Explain why my lru_cache-decorated function raised a TypeError.",
        ],
    ),
    dict(
        id="datetime-and-time",
        title="Working with Dates & Times",
        hook="Nearly every serious bug involving dates traces back to one root cause: mixing naive and timezone-aware datetime objects without realizing Python treats them as fundamentally incompatible.",
        explanation=(
            "The `datetime` module's `datetime` class represents a specific point in time; `date` represents "
            "just a calendar date with no time component; `timedelta` represents a duration, used for both "
            "computing differences between datetimes and adding/subtracting time spans (`some_date + "
            "timedelta(days=7)`). `datetime.now()` returns the current local time as a naive datetime — one "
            "with no attached timezone information at all.\n\n"
            "A 'naive' datetime has no timezone attached and represents an ambiguous point in time (is `2026-"
            "07-19 14:00` in Nairobi, New York, or UTC?), while an 'aware' datetime has a `tzinfo` attached and "
            "unambiguously represents one specific instant regardless of timezone. Python raises a `TypeError` "
            "if you try to compare or subtract a naive and an aware datetime directly — they're considered "
            "incompatible on purpose, since a meaningful comparison requires knowing both are in the same "
            "reference frame.\n\n"
            "`strftime` (string-format-time) converts a datetime object into a formatted string using format "
            "codes (`%Y-%m-%d` for a date like `2026-07-19`), and `strptime` (string-parse-time) does the "
            "reverse, parsing a string into a datetime given the expected format. Getting the format string "
            "exactly right (matching separators, padding, and case) is the most common source of parsing "
            "errors.\n\n"
            "For timezone-aware work, `zoneinfo` (built into the standard library since Python 3.9) provides "
            "IANA timezone database support — `datetime.now(ZoneInfo(\"Africa/Nairobi\"))` gives a timezone-"
            "aware datetime correctly accounting for that timezone's offset (and daylight saving rules, where "
            "applicable), which is the modern, standard-library-only replacement for the older third-party "
            "`pytz` library many existing codebases still use."
        ),
        deep_dive=(
            "Storing and comparing datetimes as naive local time is a common source of subtle bugs once an "
            "application spans multiple timezones or servers — the standard, strongly recommended practice is "
            "to store all datetimes in UTC internally (aware, with `tzinfo=timezone.utc` or `ZoneInfo(\"UTC\")`) "
            "and convert to a specific local timezone only at the point of display to a user.\n\n"
            "`timedelta` arithmetic handles calendar edge cases like month-end rollovers and leap years "
            "automatically for day-level and smaller units, but has no concept of 'a month' or 'a year' as a "
            "unit directly (since those aren't fixed durations — February isn't always the same length), which "
            "is why calendar-aware libraries like `dateutil.relativedelta` exist for 'add one month' style "
            "calculations that need to respect actual calendar rules rather than a fixed number of days.\n\n"
            "Unix timestamps (`datetime.timestamp()`, an integer or float counting seconds since 1970-01-01 "
            "UTC) are a common, unambiguous, timezone-independent way to store or transmit a point in time — "
            "converting to a timestamp and back is a reliable way to move a datetime across systems without "
            "needing to also transmit timezone metadata, as long as both ends agree to interpret it as UTC."
        ),
        code=dict(
            lang="python",
            label="Naive vs. timezone-aware datetimes",
            src=(
                "from datetime import datetime, timedelta, timezone\n\n"
                "naive = datetime.now()                          # no timezone info\n"
                "aware_utc = datetime.now(timezone.utc)          # explicitly UTC\n\n"
                "# naive - aware_utc                             # TypeError: can't mix naive and aware\n\n"
                "deadline = datetime.now() + timedelta(days=7, hours=3)\n"
                "print(deadline.strftime(\"%Y-%m-%d %H:%M\"))      # e.g. 2026-07-26 17:00\n\n"
                "parsed = datetime.strptime(\"2026-07-19\", \"%Y-%m-%d\")\n"
                "print(parsed.year, parsed.month, parsed.day)     # 2026 7 19"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Timezone conversion with zoneinfo",
            src=(
                "from datetime import datetime\n"
                "from zoneinfo import ZoneInfo\n\n"
                "utc_time = datetime.now(ZoneInfo(\"UTC\"))\n"
                "nairobi_time = utc_time.astimezone(ZoneInfo(\"Africa/Nairobi\"))\n"
                "new_york_time = utc_time.astimezone(ZoneInfo(\"America/New_York\"))\n\n"
                "print(utc_time.strftime(\"%H:%M %Z\"))\n"
                "print(nairobi_time.strftime(\"%H:%M %Z\"))\n"
                "print(new_york_time.strftime(\"%H:%M %Z\"))\n"
                "# All three represent the SAME instant, displayed in different timezones"
            ),
        ),
        example=(
            "A booking platform storing appointment times as naive local datetimes broke the moment it "
            "expanded to customers in a second timezone — every comparison and sort silently assumed the "
            "server's local time, which had no meaning for a customer in a different region. Migrating to "
            "aware UTC datetimes stored internally, converted to local time only for display, fixed the class "
            "of bug permanently."
        ),
        best_practices=[
            "Store and compute with timezone-aware UTC datetimes internally; convert to local time only when displaying to a user.",
            "Use `zoneinfo` (standard library, 3.9+) over the older third-party `pytz` for new code.",
            "Be explicit about the exact `strftime`/`strptime` format string rather than guessing — mismatched formats are a very common source of parsing errors.",
            "Use Unix timestamps for transmitting a point in time between systems when you want an unambiguous, timezone-independent representation.",
        ],
        pitfalls=[
            "Mixing naive and timezone-aware datetimes in the same comparison or subtraction, causing a `TypeError` (or worse, silently wrong results in older code that didn't enforce this).",
            "Using `datetime.now()` (local, naive) when `datetime.now(timezone.utc)` (aware, UTC) is what a multi-timezone application actually needs.",
            "Assuming `timedelta(days=30)` is equivalent to 'one month' — it isn't, since months vary in length; use a calendar-aware library for genuine month/year arithmetic.",
        ],
        glossary=[
            dict(term="Naive datetime", definition="A datetime object with no attached timezone information, representing an ambiguous point in time."),
            dict(term="Aware datetime", definition="A datetime object with tzinfo attached, unambiguously representing one specific instant in time."),
            dict(term="timedelta", definition="A duration or difference between two datetimes, usable in arithmetic with datetime objects."),
            dict(term="Unix timestamp", definition="The number of seconds since 1970-01-01 00:00:00 UTC, a common timezone-independent way to represent a point in time."),
        ],
        faq=[
            dict(q="Why did comparing two datetimes raise a TypeError?", a="One was naive and the other was timezone-aware — Python refuses to compare them directly since it can't know if the naive one is meant to be in the same timezone as the aware one."),
            dict(q="Should I always use UTC internally?", a="For anything beyond a strictly single-timezone application, yes — storing and computing in UTC, converting to local time only for display, avoids an entire category of timezone bugs as an application grows."),
            dict(q="What's the difference between zoneinfo and pytz?", a="zoneinfo is the modern standard-library module (3.9+) for IANA timezone support; pytz was the long-standing third-party solution before that. New code should prefer zoneinfo since it requires no extra dependency and has a cleaner API."),
        ],
        quiz=[
            dict(
                question="Why does Python refuse to directly compare a naive and an aware datetime?",
                options=["It's a bug that will be fixed eventually", "A naive datetime has no timezone, so the comparison would be ambiguous", "Aware datetimes are always larger", "Naive datetimes can't be created in Python 3"],
                correct=1,
                explanation="Without timezone information, there's no way to know what a naive datetime is actually relative to, so Python treats mixing them as an error rather than guessing.",
            ),
        ],
        prompts=[
            "Why does comparing these two datetime objects raise a TypeError?",
            "Show me how to convert a UTC timestamp to a specific local timezone.",
            "What's the best practice for storing datetimes in a database for a multi-timezone app?",
            "Explain the difference between zoneinfo and pytz for timezone handling.",
        ],
    ),
    dict(
        id="testing-fundamentals",
        title="Testing Fundamentals: assert & unittest",
        hook="Before reaching for pytest (covered in the Python Libraries track), it's worth understanding what Python gives you out of the box — because every testing framework you'll ever use is built on the same core idea: run code, check an assertion, report what failed.",
        explanation=(
            "The `assert` statement checks a condition and raises `AssertionError` if it's false — "
            "`assert result == expected, \"message\"` is the simplest possible test: if `result != expected`, "
            "the program halts with that message. This is the atomic building block every testing framework "
            "is built around, though bare `assert` statements scattered through application code are a "
            "different (and much weaker) tool than a proper test suite, since `assert` statements are "
            "stripped out entirely when Python runs with optimizations enabled (`python -O`).\n\n"
            "The standard library's `unittest` module provides a structured framework: test cases are methods "
            "on a class inheriting from `unittest.TestCase`, named starting with `test_` so the framework "
            "discovers them automatically. Assertion methods like `self.assertEqual(a, b)`, `self.assertTrue"
            "(x)`, and `self.assertRaises(ExceptionType)` give clearer failure messages than a bare `assert` "
            "would, showing exactly what was expected versus what was received.\n\n"
            "`setUp()` runs before every test method in a `TestCase`, and `tearDown()` runs after, giving a "
            "consistent place to prepare and clean up shared test fixtures without repeating that code in "
            "every single test method. Tests are run with `python -m unittest` or by running the test file "
            "directly if it includes the `unittest.main()` boilerplate.\n\n"
            "The core testing mindset — write code that exercises your function, compare the actual result to "
            "an expected one, and make failures loud and specific — applies identically whether you're using "
            "bare `assert`, `unittest`, or (more commonly in modern projects) `pytest`, which layers a much "
            "more ergonomic API on top of the same fundamental idea."
        ),
        deep_dive=(
            "A good test suite generally follows the Arrange-Act-Assert pattern: set up the inputs and any "
            "necessary state (Arrange), call the function or code under test (Act), and check the result "
            "against what's expected (Assert). Keeping these three phases visually distinct in each test "
            "makes tests far easier to read and maintain than tests that interleave setup, execution, and "
            "checking throughout.\n\n"
            "Testing for exceptions correctly matters: `self.assertRaises(ValueError)` used as a context "
            "manager (`with self.assertRaises(ValueError): risky_call()`) verifies that a specific exception "
            "type is raised, which is meaningfully different from — and much more precise than — wrapping the "
            "call in a try/except and manually checking a boolean flag.\n\n"
            "Mocking (via `unittest.mock`) lets you replace a real dependency (a network call, a database "
            "query, the current time) with a controllable fake during a test, so the test can run fast, "
            "deterministically, and without needing the real external system available — `unittest.mock."
            "patch()` is the standard tool for temporarily substituting an object during a test's execution."
        ),
        code=dict(
            lang="python",
            label="A unittest TestCase with setUp",
            src=(
                "import unittest\n\n"
                "def calculate_discount(price, percent):\n"
                "    if not (0 <= percent <= 100):\n"
                "        raise ValueError(\"percent must be between 0 and 100\")\n"
                "    return price * (1 - percent / 100)\n\n"
                "class TestDiscount(unittest.TestCase):\n"
                "    def setUp(self):\n"
                "        self.price = 100.0\n\n"
                "    def test_ten_percent_off(self):\n"
                "        self.assertEqual(calculate_discount(self.price, 10), 90.0)\n\n"
                "    def test_invalid_percent_raises(self):\n"
                "        with self.assertRaises(ValueError):\n"
                "            calculate_discount(self.price, 150)\n\n"
                "if __name__ == \"__main__\":\n"
                "    unittest.main()"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Mocking an external dependency during a test",
            src=(
                "from unittest.mock import patch\n"
                "import unittest\n\n"
                "def get_weather_summary(city, api_client):\n"
                "    data = api_client.fetch(city)\n"
                "    return f\"{city}: {data['temp']}C\"\n\n"
                "class TestWeather(unittest.TestCase):\n"
                "    @patch(\"__main__.requests\")\n"
                "    def test_summary_uses_fetched_data(self, mock_requests):\n"
                "        mock_client = unittest.mock.Mock()\n"
                "        mock_client.fetch.return_value = {\"temp\": 24}\n"
                "        result = get_weather_summary(\"Nairobi\", mock_client)\n"
                "        self.assertEqual(result, \"Nairobi: 24C\")   # no real API call made"
            ),
        ),
        example=(
            "A payment-processing function's test suite mocks the actual payment gateway API entirely, "
            "letting hundreds of tests covering edge cases (declined cards, network timeouts, invalid amounts) "
            "run in milliseconds without making a single real network call or risking an accidental real charge."
        ),
        best_practices=[
            "Follow Arrange-Act-Assert as a mental structure for every test, even informally, to keep tests readable.",
            "Use `assertRaises` as a context manager to test for expected exceptions precisely, rather than a manual try/except with a flag.",
            "Mock external dependencies (network, database, current time) so tests run fast and deterministically without needing those systems available.",
            "Write a failing test first when fixing a bug, confirm it fails for the right reason, then fix the code and confirm the test passes — this proves the fix actually addresses the bug.",
        ],
        pitfalls=[
            "Relying on bare `assert` statements for real test suites, which get silently stripped out entirely when Python runs with the `-O` optimization flag.",
            "Writing tests that depend on shared, mutable state or a specific execution order, causing them to pass individually but fail when run together or in a different order.",
            "Testing against a real external API or database in the main test suite, making tests slow, flaky, and dependent on that system's availability.",
        ],
        glossary=[
            dict(term="Assertion", definition="A statement checking that a condition holds, raising an error (and failing the test) if it doesn't."),
            dict(term="Test fixture", definition="The fixed baseline state or objects a test needs set up before it runs, often prepared in setUp()."),
            dict(term="Mock", definition="A fake, controllable stand-in for a real dependency, used in tests to avoid relying on real external systems."),
            dict(term="Arrange-Act-Assert", definition="A common structure for writing a test: set up inputs, run the code under test, then check the result."),
        ],
        faq=[
            dict(q="Why not just use assert statements everywhere instead of a testing framework?", a="Bare asserts give minimal failure information, aren't automatically discovered and run as a suite, and are stripped out entirely when Python runs with -O — a real testing framework provides test discovery, clear failure reports, fixtures, and reliable execution regardless of optimization flags."),
            dict(q="What's the point of mocking instead of just testing against the real system?", a="Speed, determinism, and independence — tests against a real database or API are slow, can fail for reasons unrelated to your code (network issues, rate limits), and might have unwanted side effects like real charges or emails."),
            dict(q="Is unittest still relevant if most projects use pytest?", a="Yes — pytest can run unittest-style tests, unittest.mock is still the standard mocking library even in pytest-based projects, and understanding unittest's structure makes pytest's more concise API easier to appreciate."),
        ],
        quiz=[
            dict(
                question="Why are bare assert statements risky as the sole basis for a test suite?",
                options=["They're always slower", "They're stripped out entirely when Python runs with the -O flag", "They can't check equality", "They only work inside classes"],
                correct=1,
                explanation="Python's -O optimization flag removes assert statements from the compiled bytecode entirely, meaning any tests relying purely on bare asserts would silently stop running.",
            ),
        ],
        prompts=[
            "Write a unittest TestCase for this function, including an edge case.",
            "Show me how to mock an external API call in a test.",
            "Explain the Arrange-Act-Assert pattern with an example test.",
            "Why is my test suite flaky when tests are run in a different order?",
        ],
    ),
    dict(
        id="enumerate-zip-sorting",
        title="enumerate, zip & Sorting Idioms",
        hook="Three small built-ins — enumerate, zip, and the key argument to sorted — eliminate almost every reason to manually manage an index counter in a Python loop.",
        explanation=(
            "`enumerate(iterable)` pairs each item with its index, producing `(0, first_item), (1, "
            "second_item), ...` — replacing the C-style pattern of `for i in range(len(items)): item = "
            "items[i]` with the more direct `for i, item in enumerate(items):`. An optional `start` argument "
            "(`enumerate(items, start=1)`) lets the index begin somewhere other than zero, useful for "
            "human-facing numbering.\n\n"
            "`zip(iterable_a, iterable_b, ...)` pairs up corresponding elements from multiple iterables into "
            "tuples, stopping as soon as the shortest input is exhausted — `zip(names, scores)` produces "
            "`(name, score)` pairs for iterating over two related lists in lockstep, without manual indexing "
            "into both. `zip(*pairs)` (unpacking) is the idiomatic way to 'unzip' a list of tuples back into "
            "separate lists.\n\n"
            "`sorted(iterable, key=..., reverse=...)` sorts any iterable and returns a new list, leaving the "
            "original unchanged (`list.sort()` sorts a list in place instead, returning `None`). The `key` "
            "argument is a function applied to each element to determine sort order — `sorted(people, "
            "key=lambda p: p.age)` sorts by age without needing to define a full comparison function, and "
            "`sorted(words, key=len)` sorts by length using a built-in function directly as the key.\n\n"
            "Sorting is stable in Python — elements that compare equal under the `key` function retain their "
            "original relative order — which is what makes multi-level sorts possible by sorting multiple "
            "times, least significant key first: sort by last name, then sort the result by department, and "
            "same-department entries stay sorted by last name within each department."
        ),
        deep_dive=(
            "`operator.itemgetter` and `operator.attrgetter` are often faster and more readable than an "
            "equivalent lambda for the extremely common 'sort by this field' pattern: `sorted(records, "
            "key=itemgetter(\"score\"))` for dicts, or `sorted(people, key=attrgetter(\"age\"))` for objects, "
            "both avoiding the small overhead of calling a Python-level lambda for every comparison.\n\n"
            "For a true multi-key sort in one pass rather than several stable sub-sorts, `key` can return a "
            "tuple: `sorted(people, key=lambda p: (p.department, p.last_name))` sorts primarily by "
            "department, and by last name as a tiebreaker within each department — tuples compare "
            "element-by-element, which is exactly the semantics a multi-level sort needs.\n\n"
            "`zip_longest` (from `itertools`) is the version of `zip` that doesn't stop at the shortest "
            "iterable — instead it pads missing values from shorter iterables with a specified fill value "
            "(default `None`), useful whenever you specifically need every element from the longest input "
            "iterable represented in the output, not just as many pairs as the shortest input allows."
        ),
        code=dict(
            lang="python",
            label="enumerate and zip replacing manual indexing",
            src=(
                "fruits = [\"apple\", \"banana\", \"cherry\"]\n\n"
                "for i, fruit in enumerate(fruits, start=1):\n"
                "    print(f\"{i}. {fruit}\")\n"
                "# 1. apple\n"
                "# 2. banana\n"
                "# 3. cherry\n\n"
                "names = [\"Amara\", \"Kito\", \"Zuri\"]\n"
                "scores = [94, 87, 91]\n"
                "for name, score in zip(names, scores):\n"
                "    print(f\"{name}: {score}\")"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Multi-key sorting with a tuple key and itemgetter",
            src=(
                "from operator import itemgetter\n\n"
                "employees = [\n"
                "    {\"name\": \"Amara\", \"dept\": \"Eng\", \"level\": 3},\n"
                "    {\"name\": \"Kito\", \"dept\": \"Eng\", \"level\": 1},\n"
                "    {\"name\": \"Zuri\", \"dept\": \"Sales\", \"level\": 2},\n"
                "]\n\n"
                "# Sort by department, then by level within each department\n"
                "ranked = sorted(employees, key=lambda e: (e[\"dept\"], e[\"level\"]))\n\n"
                "# Same idea, using itemgetter for a single field (slightly faster, common style)\n"
                "by_name = sorted(employees, key=itemgetter(\"name\"))"
            ),
        ),
        example=(
            "A leaderboard displaying rank, player name, and score together builds the display rows with "
            "`for rank, (name, score) in enumerate(sorted(zip(names, scores), key=lambda p: -p[1]), start=1):` "
            "— combining zip, sorted with a key, and enumerate in one idiomatic line to go from two parallel "
            "lists to a ranked, numbered display."
        ),
        best_practices=[
            "Use `enumerate()` instead of `range(len(items))` any time you need both the index and the item.",
            "Use `zip()` to iterate over two or more related sequences in lockstep instead of indexing into each manually.",
            "Use `sorted(..., key=...)` with a lambda, `itemgetter`, or `attrgetter` instead of writing a custom comparison function.",
            "Return a tuple from `key` for multi-level sorts in a single pass, rather than chaining multiple separate sorted() calls.",
        ],
        pitfalls=[
            "Forgetting that `zip()` silently stops at the shortest input, which can quietly drop data from longer iterables without any error or warning.",
            "Using `list.sort()` when you needed `sorted()` (or vice versa) — one mutates in place and returns None, the other returns a new list and leaves the original untouched.",
            "Writing a full custom comparison function when a simple `key` function would do the same job more concisely and often faster.",
        ],
        glossary=[
            dict(term="enumerate", definition="A built-in that pairs each item in an iterable with its index, avoiding manual index-tracking in a loop."),
            dict(term="zip", definition="A built-in that pairs up corresponding elements from multiple iterables, stopping at the shortest one."),
            dict(term="Sort key", definition="A function applied to each element to determine sort order, passed as the key argument to sorted() or list.sort()."),
            dict(term="Stable sort", definition="A sorting algorithm guarantee that elements comparing equal under the key retain their original relative order."),
        ],
        faq=[
            dict(q="What happens if the lists I zip() together have different lengths?", a="zip() stops as soon as it exhausts the shortest one, silently dropping any extra elements from longer iterables. Use itertools.zip_longest if you need every element from the longest iterable represented, with a fill value for the gaps."),
            dict(q="What's the difference between sorted() and list.sort()?", a="sorted() works on any iterable and returns a new list, leaving the original unchanged. list.sort() only works on lists, sorts in place, and returns None — calling print(my_list.sort()) is a common mistake that prints None."),
            dict(q="Why use itemgetter instead of a lambda for a sort key?", a="They're functionally equivalent for simple field access, but itemgetter/attrgetter are implemented in C and avoid the overhead of calling a Python-level lambda for every comparison, which matters for sorting large datasets."),
        ],
        quiz=[
            dict(
                question="What does zip([1,2,3], ['a','b']) produce when converted to a list?",
                options=["[(1,'a'), (2,'b'), (3, None)]", "[(1,'a'), (2,'b')]", "[(1,2,3), ('a','b')]", "An error"],
                correct=1,
                explanation="zip stops at the shortest iterable, so with a length-2 and a length-3 input, only 2 pairs are produced.",
            ),
            dict(
                question="What does list.sort() return?",
                options=["The sorted list", "None -- it sorts in place", "A generator", "A copy of the original unsorted list"],
                correct=1,
                explanation="list.sort() mutates the list in place and returns None, which is why print(my_list.sort()) is a common beginner mistake.",
            ),
        ],
        prompts=[
            "Show me how to sort this list of dicts by two fields at once.",
            "Why did zip() drop some of my data?",
            "Convert this manual index-based loop to use enumerate.",
            "What's the difference between sorted() and .sort(), and when do I use each?",
        ],
    ),
    dict(
        id="collections-module",
        title="The collections Module: Counter, defaultdict & deque",
        hook="Three types from the standard library's collections module quietly eliminate some of the most common boilerplate in everyday Python: counting things, grouping things, and building a queue.",
        explanation=(
            "`Counter` is a dict subclass specialized for counting hashable items — `Counter(some_list)` "
            "builds a count of every element in one call, replacing a manual loop that checks `if item in "
            "counts: counts[item] += 1 else: counts[item] = 1`. It supports `.most_common(n)` to get the top "
            "N most frequent items directly, and arithmetic between counters (`counter_a + counter_b`) that "
            "adds counts together intuitively.\n\n"
            "`defaultdict(factory)` is a dict subclass where accessing a missing key doesn't raise "
            "`KeyError` — instead, it calls `factory()` to create a default value, inserts it, and returns "
            "it. `defaultdict(list)` means every new key automatically starts as an empty list, which "
            "eliminates the common `if key not in d: d[key] = []` check before appending — you can just "
            "write `d[key].append(value)` directly, even for a key you've never seen before.\n\n"
            "`deque` (double-ended queue) supports O(1) appends and pops from *both* ends, unlike a plain "
            "list, where removing from the front is O(n) because every remaining element has to shift over. "
            "This makes `deque` the right tool for anything needing a queue (FIFO), a stack with both-end "
            "access, or a fixed-size rolling window (`deque(maxlen=n)` automatically drops the oldest item "
            "once it's full).\n\n"
            "`namedtuple` (the older, function-based predecessor to `typing.NamedTuple`) creates a lightweight, "
            "tuple-based class with named fields in one line: `Point = namedtuple(\"Point\", [\"x\", \"y\"])` "
            "gives you `Point(1, 2).x` access alongside normal tuple behavior — still seen often in existing "
            "codebases even though `typing.NamedTuple` is generally preferred for new code needing type hints."
        ),
        deep_dive=(
            "`defaultdict`'s factory function is called with zero arguments every time a missing key is "
            "accessed — this is why `defaultdict(list)` and `defaultdict(int)` work (calling `list()` gives "
            "`[]`, calling `int()` gives `0`), but a factory needing arguments requires wrapping it in a "
            "lambda: `defaultdict(lambda: {\"count\": 0, \"total\": 0.0})` for a more complex default "
            "structure.\n\n"
            "`Counter` supports set-like operations that respect counts: `counter_a & counter_b` (intersection) "
            "keeps the minimum count for each shared key, and `counter_a | counter_b` (union) keeps the "
            "maximum — genuinely useful for problems like finding the common elements between two multisets "
            "with their smaller shared frequency.\n\n"
            "`deque`'s `maxlen` parameter, combined with its O(1) append/pop from both ends, makes it the "
            "natural data structure for a 'last N events' rolling buffer — appending a new event and letting "
            "the oldest one automatically fall off the other end happens in constant time regardless of how "
            "large N is, which a list-based approach (removing from the front) would make progressively "
            "slower as more items accumulate."
        ),
        code=dict(
            lang="python",
            label="Counter and defaultdict eliminating manual boilerplate",
            src=(
                "from collections import Counter, defaultdict\n\n"
                "words = \"the cat sat on the mat the cat ran\".split()\n"
                "counts = Counter(words)\n"
                "print(counts.most_common(2))          # [('the', 3), ('cat', 2)]\n\n"
                "groups = defaultdict(list)\n"
                "for word in words:\n"
                "    groups[len(word)].append(word)     # no need to check if key exists first\n"
                "print(dict(groups))                    # {3: ['the', 'cat', 'sat', ...], 2: ['on']}"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="deque as a rolling window, and namedtuple",
            src=(
                "from collections import deque, namedtuple\n\n"
                "recent_errors = deque(maxlen=5)          # keeps only the last 5 automatically\n"
                "for i in range(10):\n"
                "    recent_errors.append(f\"error-{i}\")\n"
                "print(list(recent_errors))                # ['error-5', ..., 'error-9']\n\n"
                "Point = namedtuple(\"Point\", [\"x\", \"y\"])\n"
                "p = Point(3, 4)\n"
                "print(p.x, p.y, p[0])                     # 3 4 3 -- named AND positional access"
            ),
        ),
        example=(
            "A rate-limiting middleware tracks the timestamps of the last 100 requests per user in a "
            "`deque(maxlen=100)`, getting automatic, O(1) eviction of the oldest timestamp as new ones arrive "
            "— a plain list would require manually slicing or popping from the front, which is O(n) per "
            "request at scale."
        ),
        best_practices=[
            "Use `Counter` instead of a manual dict-based counting loop any time you're tallying occurrences of items.",
            "Use `defaultdict` instead of repeatedly checking `if key not in d` before appending or accumulating into a value.",
            "Use `deque` instead of a list whenever you need to add or remove from the front, or need a fixed-size rolling buffer.",
            "Prefer `typing.NamedTuple` over the older function-based `namedtuple` for new code where type hints matter.",
        ],
        pitfalls=[
            "Using a plain list with `.pop(0)` or `.insert(0, x)` in a loop where a `deque` would give the same behavior in O(1) instead of O(n) per operation.",
            "Passing a factory that requires arguments directly to `defaultdict` without wrapping it in a lambda, causing a `TypeError` on first missing-key access.",
            "Forgetting that `Counter` returns 0 (not `KeyError`) for a key that was never counted, which is usually convenient but can mask a genuine typo in a key name.",
        ],
        glossary=[
            dict(term="Counter", definition="A dict subclass specialized for counting hashable items, with built-in most_common() and counter arithmetic."),
            dict(term="defaultdict", definition="A dict subclass that auto-creates a default value (via a factory function) for any missing key instead of raising KeyError."),
            dict(term="deque", definition="A double-ended queue supporting O(1) append/pop from both ends, unlike a list's O(n) operations at the front."),
            dict(term="namedtuple", definition="A function that generates a lightweight, tuple-based class with named field access, predating typing.NamedTuple."),
        ],
        faq=[
            dict(q="What's the difference between Counter and a regular dict for counting?", a="A Counter behaves like a dict but returns 0 instead of raising KeyError for missing keys, and adds convenience methods like most_common() and counter arithmetic (+, -, &, |) — a plain dict requires manual boilerplate to get the same behavior."),
            dict(q="Why is deque faster than a list for queue-like operations?", a="A list is backed by a contiguous array, so removing from the front means shifting every remaining element over — O(n). A deque is implemented as a doubly-linked structure of blocks, giving O(1) operations at both ends."),
            dict(q="When should I use namedtuple versus typing.NamedTuple?", a="For new code with type hints, typing.NamedTuple is generally preferred since it integrates with static type checkers. The older function-based namedtuple still works identically at runtime and remains common in existing codebases."),
        ],
        quiz=[
            dict(
                question="What does defaultdict(list) do when you access a key that doesn't exist yet?",
                options=["Raises KeyError", "Returns None", "Creates that key with an empty list as its value and returns it", "Raises a TypeError"],
                correct=2,
                explanation="defaultdict calls its factory function (list, producing []) to create a default value for any missing key, inserting and returning it instead of raising KeyError.",
            ),
        ],
        prompts=[
            "Rewrite this manual counting loop using collections.Counter.",
            "Why is deque better than a list for a queue, specifically?",
            "Show me how to use defaultdict to group items by a computed key.",
            "When would I reach for namedtuple instead of a full class?",
        ],
    ),
]