# sq-fuzz: Quirrel under libFuzzer (clang on Linux, tools/util)
dagor_add_target(NAME sq-fuzz EXECUTABLE OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE sq_llvm_fuzzer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/sqmodules ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/include
    ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel
  COMPILE_OPTIONS PRIVATE -fsanitize=fuzzer
  LINK_OPTIONS PRIVATE -fsanitize=fuzzer
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.startup engine.ioSys engine.math
    engine.perfMon.daProfilerStub engine.osApiWrappers.messageBox.stub 1stPartyLibs.quirrel.quirrel
    1stPartyLibs.quirrel.quirrel.sqmodules
)
