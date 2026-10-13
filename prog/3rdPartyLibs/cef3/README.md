# CEF3 (Chromium Embedded Framework)

Vendored subset of CEF used to embed a Chromium-based browser (the games'
embedded browser, `DAGOR_GAME_EMBEDDED_BROWSER`). Only the libcef_dll wrapper
sources and public C++/C API headers are kept here; the prebuilt libcef
binaries of the same version are CEF's automated builds
(https://cef-builds.spotifycdn.com), pinned in `prog/cmake/sdk/manifest.cmake`
and found by `prog/cmake/find/FindCEF.cmake` (or a local copy, `CEF_ROOT`).

Upstream: https://github.com/chromiumembedded/cef (BSD license, see the
LICENSE file under each version's libcef_dll directory).

- v4896 - CEF 100.0.24, Chromium 100.0.4896.127 (branch 4896): the one built
  (`libcef_dll/CMakeLists.txt`), on the Windows x64 binaries.
- v4951 - CEF 101.0.15, Chromium 101.0.4951.54 (branch 4951): not built.
