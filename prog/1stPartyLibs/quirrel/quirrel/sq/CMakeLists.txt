# sq, upstream's Quirrel command-line interpreter, on the engine's Quirrel host, with the test.native module of the
# language's test suite (testRunner.py: the compiler, the static analyzer, the AST dumps and the execution of testData/
# and of the documentation's examples), which the tests tree runs. The engine's build replaces upstream's CMakeLists.txt.
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()
dagor_add_target(NAME sq EXECUTABLE LAX
  FILES_CMAKE sq_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ../sqmodules ../squirrel
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE
    Dagor::Quirrel engine.osApiWrappers engine.kernel engine.memory.rtl engine.baseUtil engine.ioSys
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
if(DAGOR_ENGINE_TESTS)
  dagor_add_exec_test(1stPartyLibs.quirrel.suite COMMAND ${Python3_EXECUTABLE} testRunner.py -sq $<TARGET_FILE:sq> -ci
    WORKING_DIRECTORY .. TAGS quirrel TIMEOUT 1800)
endif()
