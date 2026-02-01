# Codility Solution Scaffold

Feed this file to Claude with a problem statement pasted at the bottom.
Claude will generate a complete directory with `solution.py` and `runner.py`.

See `min-pos-int/` for a worked example of the scaffold in action.

---

You are scaffolding a Codility solution.  Follow every instruction below
exactly.  Do not improvise or skip sections.

## 1. Directory

Derive a slug from the problem title: lowercase, words joined by hyphens
(e.g. "Min Avg Two Slice" → `min-avg-two-slice`).
Create `/Users/ben/dev/codility/<slug>/` and put both files inside it.

---

## 2. solution.py

Sections must appear in this order.

### 2a. Imports

```python
import sys
import time
import unittest
import random
```

Add anything else the problem needs (e.g. `from collections import defaultdict`).

**Only Python standard library is available on codility — no third-party
packages.**  `sys`, `time`, `unittest`, `random`, `collections`, `itertools`,
`math`, `heapq`, `bisect`, etc. are all fine.  Nothing from pip.

### 2b. Algorithm implementations

Write **at least 2, ideally 3** distinct approaches.  Each one is preceded by:

```
# ---------------------------------------------------------------------------
# Algorithm N: <Name>
# O(?) time | O(?) space
# <One sentence on the approach>
# ---------------------------------------------------------------------------
```

Rules:
- Name each function `solution_<approach>` (e.g. `solution_dp`, `solution_greedy`).
- **Never mutate the input.**  Copy first if the algorithm needs to modify it.
- Aim for meaningfully different complexities so the benchmarks reveal something.

### 2c. Registry

```python
ALGORITHMS = {
    "<name>": solution_<name>,
    ...
}
```

### 2d. TestSolution — correctness, exercised against ALL algorithms

```python
class TestSolution(unittest.TestCase):
    def _check(self, <params>, expected):
        for name, fn in ALGORITHMS.items():
            with self.subTest(algorithm=name):
                self.assertEqual(fn(<params>), expected)

    # --- provided examples (every single one from the problem statement) ---
    def test_...(self):
        self._check(<input>, <expected>)

    # --- edge cases ---
    ...
```

- Every example in the problem statement becomes its own test method.
- Add edge cases: min/max input sizes, boundary values, degenerate inputs.
- `_check` runs the assertion against **all** algorithms via `subTest` —
  a failure reports exactly which algorithm broke.

### 2e. BenchmarkSolution — head-to-head timing on large inputs

```python
class BenchmarkSolution(unittest.TestCase):
    RUNS = 5                   # repetitions per case; report the min

    def _bench(self, label, <input>):
        print(f"\n    {label} (n={len(<input>):,}):")
        for name, fn in ALGORITHMS.items():
            times = []
            for _ in range(self.RUNS):
                start = time.perf_counter()
                result = fn(<input>)
                elapsed = time.perf_counter() - start
                times.append(elapsed)
            print(f"      {name:>6}: {min(times)*1000:8.3f} ms  (result={result})")

    def test_benchmarks(self):
        random.seed(42)
        # Generate 3-4 large inputs that stress different algorithmic behaviors
        # (e.g. worst case for one algo, best case for another).
        # Use N at or near the problem's stated max constraint.
        ...
```

Think about what input shapes reveal the complexity difference between your
algorithms.  A best-case for O(n log n) might still be a worst-case for O(n²),
etc.

### 2f. Entry point — copy this block exactly, only fill in the signature

Leave `SELECT_ALGORITHM` as a placeholder for now — section 4 will have you
set it after reading the benchmark results.

```python
# ---------------------------------------------------------------------------
# Codility calls this.  Tests run every invocation (~1 ms overhead) because
# codility starts a fresh process per test case — no state survives between
# calls.  We target TestSolution explicitly rather than using unittest.main(),
# which would discover tests in __main__ (codility's harness, not this file)
# and then call sys.exit().
# Flip RUN_TESTS to False before submitting.
# ---------------------------------------------------------------------------

RUN_TESTS = True

# <reasoning will go here after benchmarks are read — see section 4>
SELECT_ALGORITHM = "<first algorithm name as temporary placeholder>"

def solution(<params>):
    if RUN_TESTS:
        suite = unittest.TestSuite()
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSolution))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(BenchmarkSolution))
        result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
        if not result.wasSuccessful():
            raise RuntimeError("Unit tests failed")
    return ALGORITHMS[SELECT_ALGORITHM](<params>)
```

---

## 3. cases.py — the only per-problem file besides solution.py

Create `<slug>/cases.py`.  The shared `runner.py` at the repo root imports
two names from it:

**CASES** — list of `(description, input, expected_output)` tuples.  Mirror
every case you wrote for `TestSolution`.  `main()` calls `solution(inp)` so
this assumes single-arg problems.

**perf_test(solution, _sol)** — receives the solution function and the
solution module as arguments.  Construct a large input at or near the
problem's max N, time `solution(...)`, and compare against a known expected
value.  Use a deterministic seed (`random.seed`).  If the expected answer
isn't easy to derive analytically, use another algorithm from `_sol` as an
oracle (e.g. `expected = _sol.solution_grouped(A)`).  Return `True` on pass.

---

## 4. Iterate until green, then select the best algorithm

This is a loop.  Do not skip ahead.

### 4a. Run the runner

```
cd /Users/ben/dev/codility/<slug>
python ../runner.py
```

### 4b. If anything fails, fix and repeat

Read the error output carefully.  Edit `solution.py` (or `runner.py` if the
bug is there).  Run again.  Keep iterating until the full output is clean:
all internal suite tests pass, all benchmark cases complete, and all platform
cases pass.  Do not move to 4c until everything is green.

### 4c. Read the benchmark numbers and choose SELECT_ALGORITHM

Once everything passes, study the benchmark table that the internal suite
printed.  Make your best assessment of which algorithm to submit, weighing:

- **Worst-case complexity matters most.**  Codility tests adversarial inputs,
  not best-case ones.  An algorithm that wins on sorted data but blows up on
  random data is a bad pick.
- **Compare across all benchmark scenarios**, not just one.  The right choice
  is the one that holds up across the board at the problem's max constraint.
- **When complexities are equivalent**, prefer the one with the smallest
  constant factor on the shuffled/random benchmark — that's the closest to
  what codility will actually throw at you.

### 4d. Write the comment and set the flag

Replace the placeholder comment and value above `SELECT_ALGORITHM` with your
reasoning, citing specific benchmark numbers.  Example:

```python
# "swap" chosen: O(n) time on all inputs.  Benchmark at n=100k —
# shuffled (the adversarial shape): swap 32 ms, sort 22 ms, set 14 ms.
# sort is O(n log n) worst-case so it loses on large random inputs despite
# winning on pre-sorted data.  set and swap are both O(n); set is faster
# here due to Python overhead on the swap loop, so set is the pick.
SELECT_ALGORITHM = "set"
```

### 4e. Final run

Run `python runner.py` one more time to confirm everything still passes with
the new selection.  You are done when the output is fully green.

---

## Hard rules — do not break these under any circumstances

1. **Never use `unittest.main()` in solution.py.**  It discovers tests in
   `__main__` (codility's harness, not your file) and then calls `sys.exit()`.
   Always use `TestLoader().loadTestsFromTestCase()`.

2. **RUN_TESTS is a manual toggle**, not a runtime state flag.  Codility
   spawns a fresh process per test case — nothing persists between runs.
   The user flips it to `False` before pasting into codility.

3. **SELECT_ALGORITHM picks the submission.**  All algorithms are tested for
   correctness; only the selected one actually runs on the platform.

4. **Never mutate input arguments.**  If an algorithm needs to rearrange data,
   copy first (`list(A)`, `A[:]`, etc.).

5. **runner.py must set `_sol.RUN_TESTS = False`** after importing the module,
   or the internal suite fires on every call and buries the runner output.

6. **Only Python standard library imports.**  Codility has no third-party
   packages installed.  If you reach for numpy, sortedcontainers, or anything
   not in the stdlib, it will fail on submission.

---

## Problem statement

<paste the full problem statement here, including the required function signature>
