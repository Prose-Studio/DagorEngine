# resCleanUtil: finds (and with -clean removes) GRP/DxP files not in the resource pack list of a vromfs
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME resCleanUtil EXECUTABLE LAX
  FILES_CMAKE resClean_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)

# the tests: the files of a game root its pack list (built into a vromfs by vromfsPacker) does not reference are listed,
# validated and removed (tests/res_clean.py, in its DAGOR_TEST_OUT: the tool only lists, hashes and deletes the packs,
# so they need not come from the asset build); no arguments is its usage (exit code -1: 255 to a POSIX parent)
if(DAGOR_CDK_TESTS)
  set(usage -1)
  if(NOT WIN32)
    set(usage 255)
  endif()
  dagor_add_exec_test(resCleanUtil.usage COMMAND ${CMAKE_COMMAND} -DCODE=${usage}
    -P ${DAGOR_CMAKE_DIR}/scripts/expect_exit.cmake $<TARGET_FILE:resCleanUtil>
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  dagor_add_exec_test(resCleanUtil.clean COMMAND ${Python3_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/tests/res_clean.py
    $<TARGET_FILE:resCleanUtil> $<TARGET_FILE:vromfsPacker> WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk
    TIMEOUT 60)
endif()
