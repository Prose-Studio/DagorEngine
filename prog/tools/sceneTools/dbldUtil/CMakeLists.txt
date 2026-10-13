# dbldUtil: lists, checks and unpacks the contents of dabuild output (.dxp.bin, .grp), the effects with gravity zones
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
