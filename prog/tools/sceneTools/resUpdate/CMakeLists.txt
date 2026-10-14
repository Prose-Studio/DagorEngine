# resUpd: updates game resource packs, vromfs packs and sound banks from new vromfs (gameResPatcher)
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub gameLibs.gameResPatcher tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME resUpd EXECUTABLE LAX
  FILES_CMAKE resUpdate_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs
  BUILD_DEPENDENCIES PRIVATE ${deps}
  PROPERTIES DAGOR_EXCEPTIONS ON
  CDK
)

# the tests: an update is made of a game root's packs, which the asset build makes (daBuild, in the assets tree) and the
# repo has none of, so they check that resUpd starts and rejects what it cannot update from: no arguments (its usage,
# exit code -1: 255 to a POSIX parent), a missing new pack list vromfs, a vromfs index that does not parse (tests/)
if(DAGOR_CDK_TESTS)
  set(usage -1)
  if(NOT WIN32)
    set(usage 255)
  endif()
  set(expect_exit ${DAGOR_CMAKE_DIR}/scripts/expect_exit.cmake)
  set(root ${CMAKE_CURRENT_BINARY_DIR}/tests/root)
  set(common WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  dagor_add_exec_test(resUpd.usage COMMAND ${CMAKE_COMMAND} -DCODE=${usage} -P ${expect_exit} $<TARGET_FILE:resUpd>
    ${common})
  dagor_add_exec_test(resUpd.missing COMMAND ${CMAKE_COMMAND} -DCODE=1 -P ${expect_exit} $<TARGET_FILE:resUpd> ${root}
    ${CMAKE_CURRENT_BINARY_DIR}/tests/new/grp_hdr.vromfs.bin res ${common})
  dagor_add_exec_test(resUpd.invalid-index COMMAND ${CMAKE_COMMAND} -DCODE=1 -P ${expect_exit} $<TARGET_FILE:resUpd>
    ${root} ${CMAKE_CURRENT_SOURCE_DIR}/tests/invalid_index.blk res ${common})
endif()
