# dumpGrp: dumps game resource packs (grp), texture packs and level binaries, with the textures they reference
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  tools.libTools.util engine.drv.drv3d_stub engine.perfMon engine.gameRes engine.lib3d engine.libFx
  commonFx.commonFxGame engine.shaders engine.scene engine.coreUtil engine.shaders gameLibs.rendInst)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox)
endif()

dagor_add_target(NAME dumpGrp EXECUTABLE LAX
  FILES_CMAKE dumpGrp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)

# the tests: packs are made by the asset build (daBuild, in the assets tree) and the repo has none, so they check that
# dumpGrp starts and rejects what it cannot dump: no arguments (its usage, exit code -1: 255 to a POSIX parent), a
# missing file, files named as packs that are not, an empty one (tests/); and that the fatal error of a pack cut short
# is reported on the console, not in a message box that would hold the run (tests/fatal_report.cmake)
if(DAGOR_CDK_TESTS)
  set(usage -1)
  if(NOT WIN32)
    set(usage 255)
  endif()
  set(expect_exit ${DAGOR_CMAKE_DIR}/scripts/expect_exit.cmake)
  set(common WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  dagor_add_exec_test(dumpGrp.usage COMMAND ${CMAKE_COMMAND} -DCODE=${usage} -P ${expect_exit} $<TARGET_FILE:dumpGrp>
    ${common})
  dagor_add_exec_test(dumpGrp.missing COMMAND ${CMAKE_COMMAND} -DCODE=13 -P ${expect_exit} $<TARGET_FILE:dumpGrp>
    ${CMAKE_CURRENT_BINARY_DIR}/tests/missing.grp -dump ${common})
  foreach(pack grp dxp.bin)
    dagor_add_exec_test(dumpGrp.not-a-${pack} COMMAND ${CMAKE_COMMAND} -DCODE=13 -P ${expect_exit}
      $<TARGET_FILE:dumpGrp> ${CMAKE_CURRENT_SOURCE_DIR}/tests/not_a_pack.${pack} -dump ${common})
  endforeach()
  dagor_add_exec_test(dumpGrp.empty COMMAND ${CMAKE_COMMAND} -DCODE=13 -P ${expect_exit} $<TARGET_FILE:dumpGrp>
    ${CMAKE_CURRENT_SOURCE_DIR}/tests/empty.grp -dump ${common})
  dagor_add_exec_test(dumpGrp.fatal-report COMMAND ${CMAKE_COMMAND} -DDUMPGRP=$<TARGET_FILE:dumpGrp>
    -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/fatal_report.cmake ${common})
endif()
