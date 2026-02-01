# https://github.com/benhuckvale/codility-harness

import sys
import time
import unittest
import random


# --- Algorithm 1: Example ---


# REPLACE: rename to solution_<your_approach> and implement.
# If the problem takes multiple args (e.g. K, M, A), add them here
# and update _check, ALGORITHMS, and solution() to match.
def solution_example(A):
    """O(?) time | O(?) space

    TODO: one sentence on the approach.
    """
    pass  # REPLACE


# --- Registry ---

# REPLACE: update keys/values as you add or rename algorithms.
ALGORITHMS = {
    "example": solution_example,
}


# --- Correctness tests ---


class TestSolution(unittest.TestCase):
    """Every case is run against ALL algorithms via subTest."""

    # REPLACE: update signature to match solution's params.
    def _check(self, A, expected):
        for name, fn in ALGORITHMS.items():
            with self.subTest(algorithm=name):
                self.assertEqual(fn(A), expected)

    # --- provided examples ---
    # REPLACE: add one test method per example in the problem statement.
    def test_placeholder(self):
        self._check([3, 1, 2], None)  # REPLACE: set expected output


# --- Benchmarks ---


class BenchmarkSolution(unittest.TestCase):
    """Head-to-head timing on large inputs."""

    RUNS = 5

    # REPLACE: update signature to match solution's params.
    def _bench(self, label, A, skip=()):
        print(f"\n    {label} (N={len(A):,}):")
        for name, fn in ALGORITHMS.items():
            if name in skip:
                print(f"      {name:>16}: skipped")
                continue
            times = []
            for _ in range(self.RUNS):
                start = time.perf_counter()
                result = fn(A)
                elapsed = time.perf_counter() - start
                times.append(elapsed)
            print(f"      {name:>16}: {min(times)*1000:8.3f} ms  (result={result})")

    def test_benchmarks(self):
        random.seed(42)
        N = 100_000

        # REPLACE: generate large inputs that stress different algorithmic
        # behaviours.  Use N at or near the problem's stated max constraint.
        A_rand = [random.randint(0, 100) for _ in range(N)]
        self._bench("random", A_rand)


# --- Entry point ---

RUN_TESTS = True

# REPLACE: set to the name of whichever algorithm you want to submit,
# after reading benchmark results.
SELECT_ALGORITHM = "example"


def run_tests():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSolution))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(BenchmarkSolution))
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stderr).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError("Unit tests failed")


# REPLACE: update signature to match your problem's params.
def solution(A):
    """Codility entry point.  Flip RUN_TESTS to False before submitting.

    Tests run every invocation because codility starts a fresh process per
    test case.  Uses TestLoader (not unittest.main) to avoid discovering
    __main__ tests and calling sys.exit().
    """
    if RUN_TESTS:
        run_tests()
    return ALGORITHMS[SELECT_ALGORITHM](A)


if "--test" in sys.argv:
    run_tests()
