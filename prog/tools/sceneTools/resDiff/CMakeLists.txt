# resDiffUtil: builds patches of game resource packs (GRP/DxP) between a base and a new game root
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME resDiffUtil EXECUTABLE LAX
  FILES_CMAKE resDiff_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)

# the tests: a patch is made of the packs of two game roots, which the asset build makes (daBuild, in the assets tree)
# and the repo has none of, so they check that resDiffUtil starts and rejects what it cannot diff: no arguments (its
# usage, exit code -1: 255 to a POSIX parent), game roots without the pack list's vromfs
if(DAGOR_CDK_TESTS)
  set(usage -1)
  if(NOT WIN32)
    set(usage 255)
  endif()
  set(expect_exit ${DAGOR_CMAKE_DIR}/scripts/expect_exit.cmake)
  set(roots ${CMAKE_CURRENT_BINARY_DIR}/tests)
  set(common WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  dagor_add_exec_test(resDiffUtil.usage COMMAND ${CMAKE_COMMAND} -DCODE=${usage} -P ${expect_exit}
    $<TARGET_FILE:resDiffUtil> ${common})
  dagor_add_exec_test(resDiffUtil.missing COMMAND ${CMAKE_COMMAND} -DCODE=1 -P ${expect_exit}
    $<TARGET_FILE:resDiffUtil> ${roots}/base ${roots}/new res ${roots}/patch ${common})
endif()
