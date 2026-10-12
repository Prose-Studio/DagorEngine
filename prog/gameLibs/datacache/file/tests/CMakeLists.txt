# Data cache file backend unit tests
dagor_add_catch2_test(NAME datacacheFile-tests LAX
  TAGS gameLibs
  FILES_CMAKE tests_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub gameLibs.datacache.file
)
