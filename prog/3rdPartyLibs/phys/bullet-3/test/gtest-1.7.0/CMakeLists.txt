# Google Test 1.7.0, the test framework of Bullet's tests (all of it in one unit, src/gtest-all.cc). GTEST_LANG_CXX11:
# its own detection reads __cplusplus, which cl leaves at 199711L, and would take std::tr1's tuple, which is gone.
dagor_add_target(NAME 3rdPartyLibs.phys.bullet-3.test.gtest-1.7.0 STATIC LAX
  FILES_CMAKE gtest-1.7.0_files.cmake
  INCLUDE_DIRECTORIES PUBLIC include PRIVATE .
  COMPILE_DEFINITIONS PUBLIC GTEST_LANG_CXX11=1
)
