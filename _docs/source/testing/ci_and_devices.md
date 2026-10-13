# CI and Devices

## GitHub Actions

The workflows run on every push to `main` and every pull request into it (and on demand), with the CMake workflow
presets on Windows, Linux and macOS hosted runners; `.github/actions/setup` installs Python, CMake, Ninja and the Linux
packages and restores the SDK and compiler caches.

- `.github/workflows/cmake.yaml`: the engine's trees, `cmake --workflow --preset <host>-<tree>` for `tests-ci`,
  `msvc-tests-ci` (Windows), `cdk`, `assets` and `editor`; the Visual Studio and Xcode generators also build one test
  program.
- `.github/workflows/template.yaml`: a project from every template (`dng.py new`), its `<host>` workflow (the game,
  its content and dedicated server), its `<host>-test` workflow and its packages, checked by `prog/cmake/scripts/verify_game_packages.py`, which also runs the game's ECS tests
  in the packaged game.

Hosted runners have no GPU: the `-ci` test presets leave out the tests labeled `requires-gpu` or `requires-display`,
while their stub driver variants run the same cases on the stub 3d driver. Failed runs upload
`build/<preset>/test-artifacts`.

## Devices

Tests run on the machine that builds them. Running the test programs of a cross-compiled tree (Android, iOS) on a
device is not set up yet: those trees register only the tests they can run on the host
(`CMAKE_CROSSCOMPILING_EMULATOR`).
