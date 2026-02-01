#!/usr/bin/env python3
"""Reusable Codility test runner.

Run from inside any solution directory:

    cd <slug>
    python ../runner.py

Expects two files in the current directory:
    solution.py  — the Codility submission (defines solution(), RUN_TESTS, …)
    cases.py     — exports CASES list and perf_test(solution, _sol) function
"""

import sys
import os
import time
import unittest

# solution.py and cases.py live in the solution directory (cwd), not here.
sys.path.insert(0, os.getcwd())

import solution as _sol
_sol.RUN_TESTS = False          # keep it off during platform cases below
from solution import solution
from cases import CASES, perf_test


def run_internal_suite():
    """Run solution.py's own suite explicitly — correctness across ALL
    algorithms + benchmarks.  This is what RUN_TESTS would do inside
    solution(), but we call it once here on our own terms."""
    print("=" * 70)
    print("  INTERNAL SUITE (all algorithms)")
    print("=" * 70)
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(_sol.TestSolution))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(_sol.BenchmarkSolution))
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
    if not result.wasSuccessful():
        print("\n  Internal suite FAILED — fix before continuing.")
        sys.exit(1)
    print()


def main():
    run_internal_suite()

    passed = failed = errors = 0

    print("=" * 70)
    print(f"  CODILITY RUNNER  (selected: {_sol.SELECT_ALGORITHM})")
    print("=" * 70)

    for desc, inp, expected in CASES:
        try:
            start = time.perf_counter()
            result = solution(inp)
            elapsed = time.perf_counter() - start

            if result == expected:
                print(f"  PASS  {desc:<42} ({elapsed*1000:.2f} ms)")
                passed += 1
            else:
                print(f"  FAIL  {desc:<42} expected={expected}, got={result}")
                failed += 1
        except Exception as e:
            print(f"  ERR   {desc:<42} {type(e).__name__}: {e}")
            errors += 1

    # --- performance smoke test ---
    print("-" * 70)
    if not perf_test(solution, _sol):
        failed += 1
    else:
        passed += 1

    # --- summary ---
    print("-" * 70)
    total = passed + failed + errors
    print(f"  {passed}/{total} passed  |  {failed} failed  |  {errors} errors")
    print("=" * 70)

    sys.exit(0 if failed == 0 and errors == 0 else 1)


if __name__ == "__main__":
    main()
