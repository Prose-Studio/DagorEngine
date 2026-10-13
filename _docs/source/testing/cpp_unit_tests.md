# C++ Unit Tests

C++ tests use [Catch2](https://github.com/catchorg/Catch2) (`prog/3rdPartyLibs/catch2`) with the engine's test main,
`prog/dagorInclude/unittest/mainCatch2.inc.cpp`.

## A test target

```text
prog/gameLibs/foo/tests/
  CMakeLists.txt
  tests_files.cmake
  main.cpp
  test_foo.cpp
  references/        // optional: reference images
  data/              // optional: anything the tests read
```

`dagor_add_catch2_test` makes a console program with exceptions enabled, links Catch2 and the test environment
(`engine.unitTest`), puts it into `<build>/tests` and registers each test case as a CTest test `<name>:<case>` (see
[Running Tests](test_runner.md)). The area's CMakeLists adds the dir with the engine's tests
(`if(DAGOR_ENGINE_TESTS)`).

```cmake
# CMakeLists.txt
dagor_add_catch2_test(NAME foo-tests
  TAGS gameLibs
  FILES_CMAKE tests_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.foo engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys
    engine.math engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)

# tests_files.cmake
set(FILES main.cpp test_foo.cpp)
```

`main.cpp`:

```cpp
#include <unittest/mainCatch2.inc.cpp>
```

Tests include `<unittest/dag_unitTest.h>`, which brings the Catch2 macros, EASTL printing and the helpers below.

## Engine environment

By default only memory, the kernel and the file system are available. Define `UNITTEST_ENV` before including the main
to bring up more:

| `UNITTEST_ENV` flag | What is initialized |
|---|---|
| `UNITTEST_ENV_SETTINGS` | `settings.blk` from the data dir (`UNITTEST_SETTINGS_BLK` overrides the name) |
| `UNITTEST_ENV_CPUJOBS` | the job system |
| `UNITTEST_ENV_GPU` | settings, jobs, the 3d driver and video (window title `UNITTEST_APP_NAME`) |

```cpp
#define UNITTEST_ENV UNITTEST_ENV_GPU
#define UNITTEST_APP_NAME "fooTests"
#include <unittest/mainCatch2.inc.cpp>
```

When the 3d driver can't start the executable exits with 77 (skipped). `--gpu-driver stub` runs GPU tests on the stub
driver; tests that need real GPU results should `SKIP()` there. `CUSTOM_UNITTEST_CODE` and
`CUSTOM_UNITTEST_SHUTDOWN_CODE` add project specific setup and teardown.

## Errors and assertions

Errors logged inside a test case fail it, and so do failed `G_ASSERT`s and EASTL assertions (the code continues, as in
a release build, instead of unwinding through engine code). Fatal errors end the case. Declare errors a test provokes on
purpose:

```cpp
TEST_CASE("bad input is reported")
{
  unittest::ExpectLogerr expect("invalid header", 1); // exactly one such error, checked at scope exit
  CHECK_FALSE(parse(bad_input));
}

TEST_CASE("errors can be inspected")
{
  String errors;
  {
    unittest::CaptureLogerr capture(errors);
    run_something();
  }
  CHECK(strstr(errors, "expected text"));
}
```

## Files

| Function | Path |
|---|---|
| `unittest::data_path("x")` | the test's data dir (its source dir unless `--data-dir` is passed) |
| `unittest::artifact_path("x")` | the case's artifact dir, kept with the report |
| `unittest::scratch_dir()` | an empty writable dir for the current case |
| `unittest::http_service(url, root)` | an HTTP server for tests with `REQUIRES http_server` |

## Image checks

```cpp
CHECK_IMAGE(image, "gradient", ImageCompareParams{});           // references/gradient.png
ImageCompareParams tolerant;
tolerant.perChannelTolerance = 4;                                // a pixel is bad above this difference
tolerant.maxRms = 0.5f;                                          // whole image root mean square limit
tolerant.maxBadPixelsPercent = 0.1f;
CHECK_IMAGE(image, "lit_scene", tolerant);
```

References are looked up as `references/<name>.<variant>.png` first (the variant is the 3d driver name in GPU
tests), then `references/<name>.png`. On a mismatch the actual, reference and diff images go to the report. A missing
reference fails; `--update-references` (or `DAGOR_TEST_UPDATE_REFERENCES=1` for a CTest run) creates or replaces
references with the actual images.

## Command line

Besides the Catch2 options, test executables accept `--data-dir`, `--artifact-dir`, `--case-timeout <sec>`,
`--image-variant`, `--gpu-driver` and `--update-references`. CTest passes them; run the program directly to debug a
single case:

```bash
build/windows-tests/tests/foo-tests-dev.exe "my case name"
```
