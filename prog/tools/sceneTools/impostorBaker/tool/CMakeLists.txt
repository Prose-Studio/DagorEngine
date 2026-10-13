# impostorBaker: bakes the impostor textures of trees and other rendinsts (its drivers' runtime files next to it)
set(deps
  engine.startup
  engine.coreUtil
  engine.math
  engine.lib3d
  engine.image
  engine.shaders
  engine.workCycle
  engine.drv.drv3d_pc_multi
  engine.imgui.stub
  engine.gameRes
  engine.scene
  engine.guiBase
  engine.animChar
  engine.phys.physCommon
  commonFx.commonFxGame
  tools.libTools.assetMgr
  tools.libTools.assetMgrHlp
  tools.libTools.util
  tools.libTools.dtx
  gameLibs.rendInst
  gameLibs.rendInst.riFx.stub
  gameLibs.render
  gameLibs.render.volumetricLights.stub
  gameLibs.render.nodeBasedShader.stub
  gameLibs.ecs.rendInst.stub
  engine.daECS.gameResStub
  tools.libTools.shaderResBuilder
  tools.sceneTools.impostorBaker.impostorUtil
  3rdPartyLibs.image.libpng-1.4.22
  3rdPartyLibs.image.psdRead
  3rdPartyLibs.arc.zlib-ng
  engine.daECS.gameResStub
  gameLibs.ecs.rendInst.stub
)
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Darwin)$")
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME impostorBaker EXECUTABLE APPLICATION LAX
  FILES_CMAKE tool_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/rendInst ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
  BUILD_DEPENDENCIES PRIVATE ${deps} tools.libTools.daKernel
  CDK
)
