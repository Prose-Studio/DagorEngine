dagor_add_target(NAME plodGen EXECUTABLE APPLICATION LAX
  FILES_CMAKE standalone_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/rendInst ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/tools/sceneTools/pointCloudGen/generator
    ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE
    tools.libTools.daKernel engine.startup engine.coreUtil engine.math engine.lib3d engine.image engine.shaders
    engine.workCycle engine.drv.drv3d_pc_multi engine.gameRes engine.scene engine.guiBase engine.animChar
    engine.phys.physCommon commonFx.commonFxGame tools.libTools.assetMgr tools.libTools.assetMgrHlp tools.libTools.util
    tools.libTools.dtx gameLibs.rendInst gameLibs.rendInst.riFx.stub gameLibs.render
    gameLibs.render.volumetricLights.stub gameLibs.render.nodeBasedShader.stub gameLibs.gamePhys.collision.rendinst.stub
    gameLibs.ecs.rendInst.stub engine.daECS.gameResStub tools.libTools.shaderResBuilder
    tools.sceneTools.pointCloudGen.generator 3rdPartyLibs.image.libpng-1.4.22 3rdPartyLibs.image.psdRead
    3rdPartyLibs.arc.zlib-ng
  CDK
)
