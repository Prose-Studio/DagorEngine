# Catch2 3.8.0 (the engine's build of it replaces the upstream CMakeLists.txt; extras/Catch.cmake is upstream's CTest
# integration). Test programs get main() from <unittest/mainCatch2.inc.cpp>, see dagor_add_catch2_test().
# its headers are third-party code: the warnings of strict test code do not apply to them
dagor_add_target(NAME 3rdPartyLibs.catch2 STATIC LAX
  FILES_CMAKE catch2_files.cmake
  INCLUDE_DIRECTORIES PUBLIC src
  COMPILE_DEFINITIONS PRIVATE CATCH_AMALGAMATED_CUSTOM_MAIN
  LICENSES LICENSE.txt
  PROPERTIES DAGOR_EXCEPTIONS ON SYSTEM ON
)
