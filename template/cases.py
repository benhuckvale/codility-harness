import time
import random

# REPLACE: each tuple is (description, input, expected_output).
# For multi-param problems, input is a tuple of args, e.g. (K, M, A).
# For single-param, input is the value directly, e.g. [3, 1, 2].
# Mirror every case in TestSolution.
CASES = [
    ("placeholder",                      [3, 1, 2],   None),  # REPLACE: set expected
]


def perf_test(solution, _sol):
    """Stress test at max N; answer verified against an oracle algorithm."""
    random.seed(77)
    N = 100_000

    # REPLACE: generate a large input matching your problem's constraints.
    A = [random.randint(0, 100) for _ in range(N)]

    # REPLACE: pick an oracle algorithm to derive the expected answer.
    # e.g. expected = _sol.solution_example(A)
    expected = _sol.solution_example(A)

    start = time.perf_counter()
    result = solution(A)  # REPLACE: match signature if multi-param
    elapsed = time.perf_counter() - start

    ok = result == expected
    label = "PASS" if ok else "FAIL"
    print(f"  {label}  perf: N={N:,} random"
          f"  expected={expected}, got={result}  ({elapsed*1000:.1f} ms)")
    return ok
