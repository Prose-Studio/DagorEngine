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
