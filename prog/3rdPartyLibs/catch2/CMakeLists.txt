# Catch2 3.8.0 (the engine's build of it replaces the upstream CMakeLists.txt; extras/Catch.cmake is upstream's CTest
# integration). Test programs get main() from <unittest/mainCatch2.inc.cpp>, see dagor_add_catch2_test().
dagor_glob_sources(sources GLOB *.cpp DIRS
  src/catch2
  src/catch2/benchmark
  src/catch2/benchmark/detail
  src/catch2/generators
  src/catch2/interfaces
  src/catch2/internal
  src/catch2/matchers
  src/catch2/matchers/internal
  src/catch2/reporters
)

# its headers are third-party code: the warnings of strict test code do not apply to them
dagor_add_library(3rdPartyLibs.catch2 LAX ${sources})
target_include_directories(3rdPartyLibs.catch2 PUBLIC src)
target_compile_definitions(3rdPartyLibs.catch2 PRIVATE CATCH_AMALGAMATED_CUSTOM_MAIN)
dagor_target_licenses(3rdPartyLibs.catch2 LICENSE.txt)
set_target_properties(3rdPartyLibs.catch2 PROPERTIES DAGOR_EXCEPTIONS ON SYSTEM ON)
