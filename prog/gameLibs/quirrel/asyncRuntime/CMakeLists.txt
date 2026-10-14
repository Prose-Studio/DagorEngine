# Quirrel async runtime per VM: the sqasync binding, the "async" module and its timer queue
dagor_add_target(NAME gameLibs.quirrel.asyncRuntime STATIC
  FILES_CMAKE asyncRuntime_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)

# its tests: the scripts of tests/ run by csq, their output compared with the .expected files
if(DAGOR_ENGINE_TESTS)
  dagor_add_exec_test(gameLibs.quirrel.asyncRuntime COMMAND ${Python3_EXECUTABLE} tests/run_tests.py
    --csq $<TARGET_FILE:csq> TAGS quirrel)
endif()
