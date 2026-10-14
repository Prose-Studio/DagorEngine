# Running Tests

Tests are registered by the functions of `prog/cmake/DagorTesting.cmake` in the trees that build them, and run by CTest:
the engine's in its `tests` trees (`cmake --preset <host>-tests`; with the Quirrel tests that csq runs: its script API,
the script libraries' suites and the static analysis of the shared scripts and of dargbox's samples), dargbox's in its
`dargbox` trees (each sample runs headless on the stub driver), a project's in its client and dedicated server trees.
The target `tests` builds the programs they run (in the engine's tests trees they are part of the default build).

## Running

```bash
ctest --preset windows-tests                        # every test of the tree
ctest --preset windows-tests -L ecs -L my_game      # by label: the layer, a tag, requires-<what>
ctest --preset windows-tests -R "foo-tests:my case" -V
ctest --preset windows-tests --output-junit junit.xml
cmake --workflow --preset windows-tests             # configure, build and test in one go
```

Each test carries the CTest labels of its layer (`cpp`, `das`, `exec`, `ecs`, `scenario`), its `TAGS` and its
`REQUIRES` as `requires-gpu`, `requires-display`, `requires-network`, `requires-http_server`. A program that can't run
on the machine exits with 77 and is reported as skipped: a game test whose client starts no video driver (no GPU, as
on CI runners) does so, and on Linux a game test that requires a display when neither `DISPLAY` nor
`WAYLAND_DISPLAY` is set.

Outputs go to `build/<preset>/test-artifacts/<test>/`: native results (`junit.xml`, `dastest.json`, `events.jsonl`),
logs, screenshots and image diffs.

## Declaring tests

In the CMakeLists of the test's dir:

```cmake
dagor_add_catch2_test(NAME foo-tests
  TAGS gameLibs
  FILES_CMAKE tests_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.foo engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys
    engine.math engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
  CASE_TIMEOUT 60
)
dagor_add_das_test(myGame.logic TAGS my_game PATHS ../scripts/my_game PROJECT ../scripts/tests.das_project)
dagor_add_game_test(my_game.ecs LAYER ecs PATHS . SCENE gamedata/scenes/test.blk CASE_TIMEOUT 60)
dagor_add_exec_test(tools.foo COMMAND ${Python3_EXECUTABLE} -m unittest discover WORKING_DIRECTORY tests)
```

| Function | Test |
|---|---|
| `dagor_add_catch2_test(NAME <name> <dagor_add_target arguments> [DATA_DIR] [CASE_TIMEOUT] [ARGS])` | a Catch2 program; each case is the CTest test `<name>:<case>` |
| `dagor_add_catch2_run(<target> <name> ...)` | another run of such a program's cases with other arguments and requirements |
| `dagor_add_das_test(<name> PATHS ... [PROJECT] [ISOLATED] [WORKING_DIRECTORY])` | daScript `[test]` functions run by dastest |
| `dagor_add_game_test(<name> LAYER ecs\|scenario PATHS ... [SCENE] [CASE_TIMEOUT] [ARGS])` | `[ecs_test]` functions run by the tree's game |
| `dagor_add_exec_test(<name> COMMAND ... [WORKING_DIRECTORY])` | any command, its exit code is the result |

All of them take `TAGS <tag>...`, `REQUIRES gpu|display|network|http_server ...`, `TIMEOUT <seconds>` (600 by
default), `SERIAL` (never in parallel with other tests) and `PLATFORMS <platform>...` (nothing is registered for the
others). `REQUIRES http_server` starts an HTTP server for the test: it serves an empty writable dir, and the test reads
its URL and dir from `DAGOR_TEST_HTTP_URL` and `DAGOR_TEST_HTTP_ROOT` (`unittest::http_service` in C++).

## Reference images

Image checks compare with `references/` next to the test. `DAGOR_TEST_UPDATE_REFERENCES=1` in the environment makes
them create or replace the references with the actual images; review them before committing:

```bash
DAGOR_TEST_UPDATE_REFERENCES=1 ctest --preset windows-client -L scenario
```
