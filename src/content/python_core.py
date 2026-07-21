"""Core Python subtopics."""

SUBTOPICS = [
    dict(
        id="variables-datatypes",
        title="Variables & Data Types",
        hook="Every value in Python carries a type, and getting comfortable with that early prevents most beginner bugs.",
        explanation=(
            "Python is dynamically typed: you never declare a variable's type up front, the interpreter infers it "
            "the moment you assign a value, and a name can point to a completely different type later. Under the "
            "hood a variable is just a label bound to an object living on the heap — `x = 5` doesn't create a box "
            "called x that holds 5, it points the name x at an integer object. This is why `id()` and `is` exist: "
            "they let you check whether two names point at the exact same object, not just an equal-looking one.\n\n"
            "The built-in types split into immutable (int, float, str, tuple, frozenset, bool) and mutable "
            "(list, dict, set, bytearray). Immutability isn't a technicality — it's what makes strings and tuples "
            "safe to use as dict keys, and it's why `a = a + 1` rebinds `a` to a new int object instead of mutating "
            "the old one, while `my_list.append(1)` mutates the same list in place."
        ),
        code=dict(
            lang="python",
            label="Types, mutability, and identity",
            src=(
                "x = 5\n"
                "y = x\n"
                "print(x is y)          # True — same int object (small ints are cached)\n\n"
                "a = [1, 2, 3]\n"
                "b = a\n"
                "b.append(4)\n"
                "print(a)                # [1, 2, 3, 4] — a and b are the SAME list\n\n"
                "c = a.copy()            # new list object\n"
                "c.append(5)\n"
                "print(a, c)              # a is unaffected\n\n"
                "print(type(3.14), type('hi'), type((1, 2)))"
            ),
        ),
        example=(
            "A shopping cart function that receives a list as a default argument and appends to it will silently "
            "share state across every call — the classic 'mutable default argument' trap traces directly back to "
            "how variables bind to objects rather than copy values."
        ),
        best_practices=[
            "Use `is` only for `None`, `True`, `False`, or singleton checks — use `==` for value comparisons.",
            "Prefer immutable types (tuples, frozensets) for data that shouldn't change; it prevents accidental mutation bugs.",
            "Use type hints (`x: int = 5`) even though Python won't enforce them — tools like mypy and your IDE will.",
        ],
        pitfalls=[
            "`def f(items=[])` reuses the same list across every call with no argument — use `None` and create the list inside.",
            "Assuming `a = b` copies a mutable object when it actually just adds a second name for the same object.",
        ],
        prompts=[
            "Explain the mutable default argument trap with a real bug example.",
            "What's the difference between shallow copy and deep copy?",
            "When should I use a tuple instead of a list?",
        ],
    ),
    dict(
        id="control-flow",
        title="Control Flow: Conditionals & Loops",
        hook="If/else and loops read almost like English in Python, but the details around truthiness and `else` on loops trip up even experienced developers coming from other languages.",
        explanation=(
            "Python has no switch statement in older versions (3.10+ added `match`/`case`), so branching logic "
            "leans on `if/elif/else`, and 'truthiness' matters more than in strictly typed languages: empty "
            "collections, `0`, `0.0`, `None`, and `''` are all falsy, so `if my_list:` is the idiomatic way to check "
            "for a non-empty list instead of `if len(my_list) > 0:`.\n\n"
            "Both `for` and `while` loops support an often-unused `else` clause that runs only if the loop completes "
            "without hitting a `break` — genuinely useful for 'search and act if not found' patterns. `for` loops in "
            "Python iterate over any iterable (not an index counter), which is why `range()`, `enumerate()`, and "
            "`zip()` show up constantly: they generate the sequences you'd manually index in other languages."
        ),
        code=dict(
            lang="python",
            label="Truthiness, enumerate, and loop-else",
            src=(
                "scores = [55, 72, 90, 61]\n\n"
                "for i, score in enumerate(scores):\n"
                "    grade = 'A' if score >= 90 else 'B' if score >= 70 else 'C'\n"
                "    print(f'Student {i}: {grade}')\n\n"
                "# match/case (3.10+) reads like a real switch statement\n"
                "def describe(status):\n"
                "    match status:\n"
                "        case 200 | 201:\n"
                "            return 'success'\n"
                "        case 404:\n"
                "            return 'not found'\n"
                "        case _:\n"
                "            return 'unknown'\n\n"
                "# for/else: runs only if no break happened\n"
                "for n in range(2, 10):\n"
                "    if n % 7 == 0:\n"
                "        print('multiple of 7 found:', n)\n"
                "        break\n"
                "else:\n"
                "    print('no multiple of 7 in range')"
            ),
        ),
        example=(
            "A CSV validator that scans rows for a bad value and wants to print 'all rows valid' only if it never "
            "broke out early is exactly what for/else was designed for — no boolean flag variable required."
        ),
        best_practices=[
            "Use `if my_list:` / `if not my_list:` rather than checking `len()` against zero.",
            "Reach for `enumerate()` instead of manually tracking an index counter.",
            "Use `match/case` for multi-branch dispatch on 3.10+; it's more readable than a long elif chain.",
        ],
        pitfalls=[
            "Forgetting that `0`, `0.0`, and `''` are falsy — `if count:` silently skips a legitimate zero count.",
            "Not realizing the `else` on a loop is tied to `break`, not to whether the loop body ever ran.",
        ],
        prompts=[
            "Show me when for/else is actually useful in real code.",
            "How does Python's match/case differ from a switch statement?",
            "What counts as falsy in Python besides False and None?",
        ],
    ),
    dict(
        id="functions-scope",
        title="Functions, Arguments & Scope",
        hook="Default arguments, *args/**kwargs, and closures are what let Python functions flex from a one-liner to a flexible API.",
        explanation=(
            "Python functions are first-class objects — you can assign them to variables, pass them as arguments, "
            "and return them from other functions. Arguments can be positional, keyword, or both, and `*args` / "
            "`**kwargs` let a function accept an arbitrary number of them, which is how most decorators and "
            "wrapper functions stay generic.\n\n"
            "Scope resolution follows the LEGB rule: Local, Enclosing, Global, Built-in — Python looks for a name "
            "in that order. A nested function can read a variable from its enclosing function automatically, but "
            "writing to it requires the `nonlocal` keyword, just as writing to a module-level variable from inside "
            "a function requires `global`. This is also the mechanism behind closures: a nested function that "
            "references a variable from its enclosing scope keeps that variable alive even after the outer "
            "function has returned."
        ),
        code=dict(
            lang="python",
            label="*args, **kwargs, and a closure",
            src=(
                "def build_request(url, *args, method='GET', **headers):\n"
                "    print(method, url, args, headers)\n\n"
                "build_request('/users', 1, 2, method='POST', Authorization='Bearer xyz')\n\n"
                "# closure: make_multiplier 'remembers' factor after it returns\n"
                "def make_multiplier(factor):\n"
                "    def multiply(n):\n"
                "        return n * factor\n"
                "    return multiply\n\n"
                "double = make_multiplier(2)\n"
                "triple = make_multiplier(3)\n"
                "print(double(5), triple(5))   # 10 15"
            ),
        ),
        example=(
            "Building a small plugin system where each 'handler' function is generated by a factory function that "
            "bakes in configuration (an API base URL, a timeout) is a closure used in production, not just a "
            "textbook demo."
        ),
        best_practices=[
            "Name `*args` and `**kwargs` something more specific when the API is public — it documents intent.",
            "Prefer keyword-only arguments (after a `*`) for options that shouldn't be passed positionally.",
            "Keep functions small enough that their scope is obvious at a glance — deep nesting hides bugs.",
        ],
        pitfalls=[
            "Forgetting `nonlocal` when trying to reassign (not mutate) a variable from an enclosing scope.",
            "Confusing `*args` (a tuple of positional extras) with `**kwargs` (a dict of keyword extras).",
        ],
        prompts=[
            "Give me a real-world example of a closure in a Flask or Django app.",
            "Explain the LEGB scope rule with a nested function example.",
            "When should I use keyword-only arguments?",
        ],
    ),
    dict(
        id="oop",
        title="Object-Oriented Programming",
        hook="Classes, inheritance, and dunder methods are how Python lets your own objects behave like built-in ones.",
        explanation=(
            "A Python class bundles data (attributes) and behavior (methods). `__init__` sets up instance state, "
            "`self` is the explicit first parameter every instance method receives (Python doesn't hide it the way "
            "some languages do), and 'dunder' methods like `__str__`, `__eq__`, `__len__`, and `__add__` are how "
            "you make a custom class work with `print()`, `==`, `len()`, and `+` respectively — this is what people "
            "mean by 'Pythonic' operator overloading.\n\n"
            "Inheritance lets a subclass reuse and extend a parent's behavior; `super()` calls the parent's "
            "implementation without hardcoding the parent's name, which matters once you're dealing with multiple "
            "inheritance and Python's MRO (Method Resolution Order). Composition — building a class out of other "
            "objects instead of inheriting from them — is often the better default; reach for inheritance only "
            "when there's a genuine 'is-a' relationship."
        ),
        code=dict(
            lang="python",
            label="Dunder methods and inheritance",
            src=(
                "class Money:\n"
                "    def __init__(self, cents):\n"
                "        self.cents = cents\n\n"
                "    def __add__(self, other):\n"
                "        return Money(self.cents + other.cents)\n\n"
                "    def __repr__(self):\n"
                "        return f'${self.cents / 100:.2f}'\n\n"
                "class DiscountedMoney(Money):\n"
                "    def __init__(self, cents, discount_pct):\n"
                "        super().__init__(cents)\n"
                "        self.cents = int(cents * (1 - discount_pct / 100))\n\n"
                "print(Money(500) + Money(250))     # $7.50\n"
                "print(DiscountedMoney(1000, 20))    # $8.00"
            ),
        ),
        example=(
            "An e-commerce codebase modeling `Money` this way means `total = price + tax + shipping` just works, "
            "with rounding rules enforced in one place instead of scattered across every calculation site."
        ),
        best_practices=[
            "Favor composition over inheritance unless there's a true 'is-a' relationship.",
            "Implement `__repr__` on every class you'll debug — it makes `print()` and the REPL actually useful.",
            "Use `@dataclass` for simple data-holding classes instead of hand-writing `__init__` and `__eq__`.",
        ],
        pitfalls=[
            "Deep inheritance chains that make it hard to know which class actually defines a given method.",
            "Forgetting `super().__init__()` in a subclass, leaving parent attributes unset.",
        ],
        prompts=[
            "Show me when to use @dataclass instead of a regular class.",
            "Explain Python's Method Resolution Order with a multiple-inheritance example.",
            "Give a real example of operator overloading that isn't just Money.",
        ],
    ),
    dict(
        id="comprehensions-generators",
        title="Comprehensions & Generators",
        hook="Comprehensions replace most manual for-loops that build a list, dict, or set; generators do the same thing without holding everything in memory at once.",
        explanation=(
            "A list comprehension `[expr for item in iterable if condition]` builds the entire result in memory "
            "before you can use any of it. A generator expression — identical syntax but with parentheses instead "
            "of brackets — yields one item at a time, lazily, which means it can represent an infinite or huge "
            "sequence using constant memory. `yield` inside a regular function turns it into a generator function: "
            "calling it doesn't run the body immediately, it returns a generator object that runs up to the next "
            "`yield` each time you call `next()` on it.\n\n"
            "Dict and set comprehensions follow the same pattern (`{k: v for ...}`, `{expr for ...}`). The rule of "
            "thumb: reach for a generator whenever you're going to iterate once and don't need `len()`, indexing, "
            "or to reuse the sequence — it's strictly cheaper."
        ),
        code=dict(
            lang="python",
            label="List comp vs generator, and a generator function",
            src=(
                "# eager — builds the whole list now\n"
                "squares = [n**2 for n in range(1_000_000)]\n\n"
                "# lazy — one item at a time, constant memory\n"
                "squares_lazy = (n**2 for n in range(1_000_000))\n"
                "print(next(squares_lazy))   # 0\n\n"
                "def read_large_file(path):\n"
                "    with open(path) as f:\n"
                "        for line in f:\n"
                "            yield line.strip()\n\n"
                "# nothing is read into memory until you iterate\n"
                "for line in read_large_file('access.log'):\n"
                "    if 'ERROR' in line:\n"
                "        print(line)"
            ),
        ),
        example=(
            "Processing a 10 GB log file line-by-line with a generator function keeps memory usage flat, where "
            "`lines = file.readlines()` would try to load the entire file into RAM first."
        ),
        best_practices=[
            "Default to a generator expression unless you specifically need `len()`, indexing, or multiple passes.",
            "Keep comprehensions to one line of real logic — nested comprehensions inside comprehensions hurt readability fast.",
            "Use `itertools` (`chain`, `islice`, `groupby`) alongside generators instead of reinventing them.",
        ],
        pitfalls=[
            "Trying to iterate a generator twice — once exhausted, it's empty, unlike a list.",
            "Writing a triple-nested comprehension that's genuinely harder to read than the equivalent for-loop.",
        ],
        prompts=[
            "Show me a real use case where a generator saves significant memory.",
            "What's the difference between yield and return?",
            "How do itertools.chain and itertools.islice work with generators?",
        ],
    ),
    dict(
        id="decorators-context-managers",
        title="Decorators & Context Managers",
        hook="Decorators wrap a function to add behavior without touching its code; context managers guarantee cleanup happens even when something goes wrong.",
        explanation=(
            "A decorator is a function that takes a function and returns a new function that wraps it — the `@` "
            "syntax is just sugar for `my_func = decorator(my_func)`. This is how logging, timing, caching "
            "(`functools.lru_cache`), and access control get bolted onto a function without changing its internals. "
            "`functools.wraps` matters because without it, the wrapped function loses its original name and "
            "docstring, which breaks introspection and debugging tools.\n\n"
            "A context manager is anything that implements `__enter__` and `__exit__` (or is built with "
            "`@contextlib.contextmanager`), used with the `with` statement. `__exit__` runs even if an exception "
            "was raised inside the block, which is exactly why files, database connections, and locks are opened "
            "with `with` — the cleanup is guaranteed, not just hoped for."
        ),
        code=dict(
            lang="python",
            label="A timing decorator and a custom context manager",
            src=(
                "import time\n"
                "import functools\n\n"
                "def timed(func):\n"
                "    @functools.wraps(func)\n"
                "    def wrapper(*args, **kwargs):\n"
                "        start = time.perf_counter()\n"
                "        result = func(*args, **kwargs)\n"
                "        print(f'{func.__name__} took {time.perf_counter() - start:.4f}s')\n"
                "        return result\n"
                "    return wrapper\n\n"
                "@timed\n"
                "def slow_sum(n):\n"
                "    return sum(range(n))\n\n"
                "from contextlib import contextmanager\n\n"
                "@contextmanager\n"
                "def db_transaction(conn):\n"
                "    try:\n"
                "        yield conn\n"
                "        conn.commit()\n"
                "    except Exception:\n"
                "        conn.rollback()\n"
                "        raise\n\n"
                "# with db_transaction(conn) as c:\n"
                "#     c.execute('UPDATE ...')"
            ),
        ),
        example=(
            "A payments service wraps every write to the ledger table in a context manager that commits on success "
            "and rolls back on any exception — one place enforces that behavior instead of every call site needing "
            "its own try/except."
        ),
        best_practices=[
            "Always apply `@functools.wraps(func)` inside a decorator so the wrapped function keeps its identity.",
            "Use `contextlib.contextmanager` for simple context managers instead of writing a full class with `__enter__`/`__exit__`.",
            "Stack decorators deliberately — order matters, the closest one to the function runs first.",
        ],
        pitfalls=[
            "Forgetting that a decorator without `*args, **kwargs` breaks any function whose signature it doesn't match exactly.",
            "Opening a resource without `with` and relying on garbage collection to close it — timing isn't guaranteed.",
        ],
        prompts=[
            "Show me a real logging decorator used in production code.",
            "How do context managers work with `with` under the hood?",
            "What does functools.lru_cache actually do, and when should I use it?",
        ],
    ),
    dict(
        id="error-handling",
        title="Error Handling & Exceptions",
        hook="try/except in Python is designed to be used deliberately, not as a catch-all — the exception hierarchy is there to help you be specific.",
        explanation=(
            "Python exceptions form a class hierarchy rooted at `BaseException`, with `Exception` as the parent of "
            "almost everything you'll actually catch. Catching a specific exception (`except ValueError:`) instead "
            "of a bare `except:` matters because a bare except also swallows `KeyboardInterrupt` and genuine bugs "
            "like `NameError`, hiding problems instead of handling them.\n\n"
            "The full try/except/else/finally structure has a purpose for each clause: `else` runs only if no "
            "exception occurred (keeping the 'happy path' separate from error handling), and `finally` always runs, "
            "exception or not, making it the right place for cleanup that isn't already handled by a context "
            "manager. Custom exceptions (subclassing `Exception`) let you build a vocabulary specific to your "
            "application instead of overloading generic ones."
        ),
        code=dict(
            lang="python",
            label="Specific exceptions, else, finally, and a custom exception",
            src=(
                "class InsufficientFundsError(Exception):\n"
                "    def __init__(self, balance, amount):\n"
                "        super().__init__(f'Cannot withdraw {amount}, balance is {balance}')\n"
                "        self.balance = balance\n\n"
                "def withdraw(balance, amount):\n"
                "    if amount > balance:\n"
                "        raise InsufficientFundsError(balance, amount)\n"
                "    return balance - amount\n\n"
                "try:\n"
                "    new_balance = withdraw(100, 150)\n"
                "except InsufficientFundsError as e:\n"
                "    print('Blocked:', e)\n"
                "except (ValueError, TypeError) as e:\n"
                "    print('Bad input:', e)\n"
                "else:\n"
                "    print('Success, new balance:', new_balance)\n"
                "finally:\n"
                "    print('Transaction logged')"
            ),
        ),
        example=(
            "A payment API that raises `InsufficientFundsError` instead of a generic `ValueError` lets the calling "
            "code show the user a specific message and lets logging/monitoring distinguish 'business rule "
            "violation' from 'actual bug' at a glance."
        ),
        best_practices=[
            "Catch the most specific exception type you can — never use a bare `except:`.",
            "Create custom exception classes for domain-specific errors instead of raising generic `Exception`.",
            "Use `finally` (or a context manager) for cleanup that must happen regardless of success or failure.",
        ],
        pitfalls=[
            "Using a bare `except:` that silently swallows `KeyboardInterrupt` and real bugs alongside expected errors.",
            "Raising and catching exceptions for normal control flow instead of for genuinely exceptional cases.",
        ],
        prompts=[
            "When should I create a custom exception class versus using a built-in one?",
            "Explain the difference between except, else, and finally with an example.",
            "Show me how exception chaining with 'raise ... from ...' works.",
        ],
    ),
    dict(
        id="file-io-modules",
        title="File I/O & Modules",
        hook="Reading files safely and organizing code into modules and packages is what turns a script into a maintainable project.",
        explanation=(
            "`open()` combined with `with` is the standard way to read or write a file — the file handle closes "
            "automatically even if an exception is raised mid-read. Text mode (`'r'`) decodes bytes to `str` using "
            "an encoding (default depends on platform, so pass `encoding='utf-8'` explicitly for portability); "
            "binary mode (`'rb'`) hands you raw bytes, needed for images, PDFs, or anything non-text.\n\n"
            "A single `.py` file is a module; a directory containing an `__init__.py` (or, since Python 3.3, even "
            "without one) is a package. `import` and `from ... import ...` pull names into your namespace, and "
            "the `if __name__ == '__main__':` guard is what lets a file work both as a standalone script and as an "
            "importable module without its top-level code firing on import."
        ),
        code=dict(
            lang="python",
            label="Safe file I/O and the __main__ guard",
            src=(
                "# writing and reading text safely\n"
                "with open('report.txt', 'w', encoding='utf-8') as f:\n"
                "    f.write('Q3 revenue: $482,000\\n')\n\n"
                "with open('report.txt', encoding='utf-8') as f:\n"
                "    for line in f:\n"
                "        print(line.strip())\n\n"
                "# pathlib is the modern, cross-platform way to handle paths\n"
                "from pathlib import Path\n"
                "data_dir = Path('data')\n"
                "csv_files = list(data_dir.glob('*.csv'))\n\n"
                "def main():\n"
                "    print('Running as a script')\n\n"
                "if __name__ == '__main__':\n"
                "    main()"
            ),
        ),
        example=(
            "A data pipeline script that's both run directly (`python pipeline.py`) and imported by a test suite "
            "relies entirely on the `__name__ == '__main__'` guard to avoid re-running the pipeline every time a "
            "test imports it."
        ),
        best_practices=[
            "Always use `with open(...)` rather than manually calling `.close()`.",
            "Pass `encoding='utf-8'` explicitly — default encoding is platform-dependent and a common source of bugs.",
            "Prefer `pathlib.Path` over raw string path manipulation for cross-platform code.",
        ],
        pitfalls=[
            "Opening a file without `with` and forgetting to close it, leaking file handles.",
            "Writing top-level code that runs side effects on import because there's no `__main__` guard.",
        ],
        prompts=[
            "What's the difference between text mode and binary mode when opening a file?",
            "Explain how Python packages and __init__.py actually work.",
            "Show me a real example of using pathlib instead of os.path.",
        ],
    ),
]
