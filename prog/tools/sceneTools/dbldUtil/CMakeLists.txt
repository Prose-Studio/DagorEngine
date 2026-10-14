# dbldUtil: exports, imports, dumps and strips the fields of level binaries (DBLD, exported by daEditor) and lists the
# resources they depend on; the effects with gravity zones
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.coreUtil
  engine.math tools.libTools.util tools.libTools.dtx engine.shaders engine.lib3d engine.gameRes engine.anim
  engine.animChar engine.phys.physCommon engine.phys.fastPhys engine.scene engine.image engine.libFx
  commonFx.commonFxGame gameLibs.render gameLibs.rendInst gameLibs.rendInst.riFx.stub
  gameLibs.render.volumetricLights.stub gameLibs.render.nodeBasedShader.stub gameLibs.landMesh engine.drv.drv3d_stub
  engine.perfMon engine.guiBase engine.imgui.stub engine.daECS.gameResStub gameLibs.ecs.rendInst.stub)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox)
endif()

dagor_add_target(NAME dbldUtil EXECUTABLE LAX
  FILES_CMAKE dbldUtil_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
  PROPERTIES DAGOR_DAFX_GRAVITY_ZONE ON
)

# the tests: level binaries (DBLD) are exported by daEditor (the editor tree) and the repo has none, so they check that
# dbldUtil starts and rejects what it cannot read: no arguments (its usage, exit code -1: 255 to a POSIX parent), a
# missing file, a file that is not a level binary (tests/)
if(DAGOR_CDK_TESTS)
  set(usage -1)
  if(NOT WIN32)
    set(usage 255)
  endif()
  set(expect_exit ${DAGOR_CMAKE_DIR}/scripts/expect_exit.cmake)
  set(common WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  dagor_add_exec_test(dbldUtil.usage COMMAND ${CMAKE_COMMAND} -DCODE=${usage} -P ${expect_exit} $<TARGET_FILE:dbldUtil>
    ${common})
  dagor_add_exec_test(dbldUtil.missing COMMAND ${CMAKE_COMMAND} -DCODE=13 -P ${expect_exit} $<TARGET_FILE:dbldUtil> PC
    ${CMAKE_CURRENT_BINARY_DIR}/tests/missing.level.bin -dump ${common})
  dagor_add_exec_test(dbldUtil.not-a-level COMMAND ${CMAKE_COMMAND} -DCODE=13 -P ${expect_exit} $<TARGET_FILE:dbldUtil>
    PC ${CMAKE_CURRENT_SOURCE_DIR}/tests/not_a_level.bin -dump ${common})
endif()
