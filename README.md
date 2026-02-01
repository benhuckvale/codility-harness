# Codility Solution Framework

A local development harness for
[Codility](https://app.codility.com/programmers/) problems. Each solution is a
single self-contained `solution.py` that runs its own tests and benchmarks —
both locally via a shared runner and on Codility itself via an embedded test
toggle.  No changes are needed before pasting into the platform (other than
flipping one flag). There is only support for Python solutions.

## Copyright

This repo contains only the scaffolding infrastructure. No Codility problem
statements are checked in as they are copyrighted. Indeed solutions are not
checked in either — solution directories are intentionally left untracked.
Any fork of this project must follow the same practice: do not commit Codility
problem text.

## Structure

Each problem lives in its own directory (e.g. `<slug>/`) with two files:

- **solution.py** — multiple algorithm implementations, a correctness suite
  exercised against all of them, head-to-head benchmarks, and a `solution()`
  entry point. A `RUN_TESTS` flag controls whether the embedded suite fires;
  flip it to `False` before submitting. `SELECT_ALGORITHM` picks which
  algorithm actually runs on the platform.
- **cases.py** — a flat list of test cases and a large-input performance smoke
  test, both consumed by the shared runner.

## Runner

`runner.py` is shared across all problems. It:

1. Runs the internal suite — correctness across all algorithms, plus benchmarks.
2. Replays every case from `cases.py` against the selected algorithm.
3. Runs the performance smoke test, verified against an oracle.

It introspects `solution()`'s signature so multi-argument problems
(e.g. `solution(S, P, Q)`) work without any tuple-packing — the entry point
keeps its native Codility signature.

## Commands

```
pdm run <slug>        # run a single problem
pdm run test-all      # run every problem in the repo
pdm run lint          # ruff check
pdm run fmt           # ruff format
```


## Manual solution building

Just copy the template/ directory to a new directory name, and start filling
out the solution.py (and cases.py) within it. Add a `tool.pdm.scripts` entry
to pyproject.toml to run it if that is useful.

The harness pays for itself on harder problems where you're iterating on
correctness, but adds overhead on straightforward ones. If you're aiming to
complete a problem fast without AI assistance, practise with the template
beforehand so the setup becomes automatic.


## AI solution building

### Scaffolding

If the problem is to be solved with AI tools `TEMPLATE_PROMPT.md` is a prompt
fed to an AI with a problem statement appended.  It produces the full
directory: several algorithms at meaningfully different complexities, a
correctness suite, benchmarks, and the selection reasoning. The workflow it
enforces:

1. Generate algorithms and tests.
2. Run until everything passes.
3. Read the benchmark output and pick the best algorithm, citing specific numbers.
4. Lint and do a final run.


## Philosophy

Codility explicitly allows candidates to work outside the IDE and paste
solutions back in. For manual solution creation, this framework facilitates
having a proper test infrastructure to solve the problem, because Codility's
platform itself is inadequate for that.

If AI is used to craft a solution this framework structures that use
deliberately rather than leaving it ad hoc. Ideally the goal is to produce
*both* a correct solution that passes 100% on the platform *and* evidence that
the candidate engaged with the problem themselves.  This is why each
solution.py could optionally include a `solution_own_attempt()` written by the
candidate alongside the AI-generated algorithms. All are tested for correctness
via the same suite, but `SELECT_ALGORITHM` picks which one actually runs on
Codility. The candidate's own attempt doesn't have to be the fastest — it just
has to be there, verified correct, and visible in the benchmarks.

Honest and transparency should apply to the infrastructure itself. The value of
this repo as evidence is that its author designed and built it — the prompt
engineering, the testing harness, the benchmark-driven selection workflow.
Someone else using this repo as-is for their own assessment wouldn't carry that
evidential weight, because it wouldn't represent their own effort in figuring
out how to orchestrate their manual work or how to orchestrate AI effectively.
The ideas and patterns here are fair game to learn from; the infrastructure
itself is not something to hand in as your own.
