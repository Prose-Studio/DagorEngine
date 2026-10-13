# Overview

Tests of the engine and of game projects are CTest tests, declared next to their sources in the CMakeLists of their
dir and run with `ctest` in the tree that builds them (see [Running Tests](test_runner.md)). Every test belongs to one
of these layers, which is its CTest label:

| Layer | What runs | Written in | Typical use |
|---|---|---|---|
| `cpp` | a Catch2 program, each case a CTest test | C++ | engine and gameLibs code, GPU code, image output |
| `das` | daScript `[test]` functions in the das interpreter | daScript | pure game logic, daslib code |
| `ecs` | `[ecs_test]` functions inside the real game (the headless dedicated server, or a single-player game headless) | daScript | entity systems, templates, gameplay rules over many frames |
| `scenario` | `[ecs_test]` functions inside the rendering client | daScript | end-to-end behavior, input, screenshots compared with references |
| `exec` | any command, its exit code is the result | anything | tools with their own test harness, Python tests |

## Quick start

In the engine's `prog/`:

```bash
cmake --workflow --preset windows-tests         # configure, build and run the tests
ctest --preset windows-tests                    # every test of the built tree
ctest --preset windows-tests -L das             # one layer
ctest --preset windows-tests -R "^datablock"    # tests whose name matches
```

A project made with `dng.py new` runs its own the same way in its `prog/` (`cmake --workflow --preset <host>-test`);
every layer has an example there (see [Creating a Project](../getting-started/new_project.md)).

## Results

Every test program, whatever the layer, reports with the same exit codes:

| Code | Meaning |
|---|---|
| 0 | all tests passed |
| 1 | a test failed (or the code under test crashed) |
| 2 | infrastructure error: the tests could not run properly |
| 3 | timeout: a test case ran longer than its limit |
| 77 | skipped: the environment can't run these tests (e.g. no GPU); CTest reports it as skipped |

## Rules all layers share

- **Errors fail tests.** Anything logged with `logerr` while a test runs fails it, unless the test declares it expected
  (`unittest::ExpectLogerr` in C++, `expect_logerr` in daScript). Errors from other threads are attributed to the test
  that was running.
- **Hangs are bounded.** A per-case timeout (`CASE_TIMEOUT`) makes the program report the case that hung and exit; the
  test's `TIMEOUT` bounds the whole run.
- **Determinism.** In-game tests advance a fixed game time per frame and ignore physical input devices; image checks
  compare against checked-in references with explicit tolerances.
