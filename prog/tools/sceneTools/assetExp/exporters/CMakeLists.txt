# The exporters of daBuild, one plugin per asset type: animations (a2dExp), anim chars, collision, fast physics, effects,
# impostors, land classes, local shaders, materials, models (rendinsts, dynamic models, skeletons, grass), physics
# objects and textures. (jam's static exporters library is for the static daBuild, which no build uses.)
add_subdirectory(scriptHelpersLt)

include(../dabuildPlugin.cmake)
set(shared ${DAGOR_PROG_DIR}/tools/sharedInclude)
set(editor ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include)
set(images 3rdPartyLibs.image.avif 3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.image.psdRead 3rdPartyLibs.image.tiff-4.4.0
  3rdPartyLibs.image.libpng-1.4.22 3rdPartyLibs.arc.zlib-ng)

dabuild_plugin(a2dExp a2dExp.cpp a2dOptimizer.cpp exp_skeleton_tools.cpp exp_tools.cpp)
target_include_directories(a2dExp PRIVATE ${shared} ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes)
target_link_libraries(a2dExp PRIVATE engine.startup tools.libTools.assetMgr engine.math engine.lib3d
  engine.drv.drv3d_null tools.libTools.shaderResBuilder tools.libTools.dagFileRW)
dabuild_plugin(animCharExp animCharExp.cpp exp_animTree.cpp exp_stateGraph.cpp exp_animChar.cpp)
target_include_directories(animCharExp PRIVATE ${shared})
target_link_libraries(animCharExp PRIVATE engine.startup engine.math engine.perfMon tools.libTools.assetMgr
  tools.libTools.pageAsg engine.lib3d engine.shaders engine.gameRes engine.scene engine.drv.drv3d_null
  tools.libTools.shaderResBuilder tools.libTools.dagFileRW tools.libTools.ambientOcclusion)
dabuild_plugin(collisionExp exp_tools.cpp exp_collision.cpp)
target_include_directories(collisionExp PRIVATE ${shared} ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/math/vhacd)
target_link_libraries(collisionExp PRIVATE engine.startup engine.math engine.lib3d engine.drv.drv3d_null engine.gameRes
  engine.scene engine.coreUtil tools.libTools.assetMgr tools.libTools.dagFileRW tools.libTools.math
  tools.libTools.collision 3rdPartyLibs.math.vhacd)
dabuild_plugin(fastPhysExp fastPhysExp.cpp)
target_include_directories(fastPhysExp PRIVATE ${shared})
target_link_libraries(fastPhysExp PRIVATE engine.startup engine.math engine.perfMon tools.libTools.assetMgr
  tools.libTools.fastPhysData tools.libTools.dagFileRW)
dabuild_plugin(fxExp fxExp.cpp fxExpStubs.cpp)
target_include_directories(fxExp PRIVATE ${shared})
target_link_libraries(fxExp PRIVATE engine.startup engine.math engine.lib3d engine.drv.drv3d_null engine.consoleProc
  tools.libTools.assetMgr tools.libTools.dagFileRW tools.sceneTools.assetExp.exporters.scriptHelpersLt
  commonFx.commonFxTools 3rdPartyLibs.math.srcc_msu)
dabuild_plugin(impostorExp exp_impostorData.cpp)
target_include_directories(impostorExp PRIVATE ${shared} ${editor})
target_link_libraries(impostorExp PRIVATE engine.startup tools.libTools.assetMgr)
dabuild_plugin(landClsExp landClsExp.cpp landClsExpStubs.cpp)
target_include_directories(landClsExp PRIVATE ${shared} ${editor})
target_link_libraries(landClsExp PRIVATE engine.startup engine.image 3rdPartyLibs.hash tools.libTools.assetMgr
  tools.sceneTools.daEditorX.services.bitMaskMgr)
dabuild_plugin(locShadersExp locShadersExp.cpp)
target_include_directories(locShadersExp PRIVATE ${shared})
target_link_libraries(locShadersExp PRIVATE engine.startup engine.math tools.libTools.assetMgr)
dabuild_plugin(matExp matExp.cpp)
target_include_directories(matExp PRIVATE ${shared})
target_link_libraries(matExp PRIVATE engine.startup engine.math engine.lib3d tools.libTools.assetMgr
  tools.libTools.dagFileRW)
dabuild_plugin(modelExp modelExp.cpp modelExpUtil.cpp exp_tools.cpp exp_skeleton_tools.cpp exp_rendInst.cpp
  exp_dynModel.cpp exp_skeleton.cpp exp_rndGrass.cpp)
target_include_directories(modelExp PRIVATE ${shared} ${DAGOR_PROG_DIR}/engine/sharedInclude)
target_compile_definitions(modelExp PRIVATE _DEBUG_TAB_)
target_link_libraries(modelExp PRIVATE engine.startup engine.math engine.lib3d engine.shaders engine.drv.drv3d_null
  engine.gameRes engine.scene engine.perfMon tools.libTools.assetMgr tools.libTools.shaderResBuilder
  tools.libTools.dagFileRW engine.image tools.libTools.ambientOcclusion ${images})
dabuild_plugin(phObjExp phObjExp.cpp phSysObj.cpp)
target_include_directories(phObjExp PRIVATE ${shared})
target_link_libraries(phObjExp PRIVATE engine.startup engine.math engine.lib3d engine.drv.drv3d_null
  tools.libTools.assetMgr tools.libTools.dagFileRW)
# textures: the DDSx conversion of every format, ASTC through the astcenc programs next to the tools, BC/ETC through
# the ISPC texture compressor
set(tex_includes ${shared} ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/nvtt-2.0.7 ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(tex_defines)
set(tex_deps engine.startup engine.image engine.math tools.libTools.assetMgr 3rdPartyLibs.convert.nvtt-2.0.7 ${images}
  3rdPartyLibs.eastl)
if(DAGOR_ARCH STREQUAL "e2k")
  set(tex_defines TEX_CANNOT_USE_ISPC)
else()
  list(APPEND tex_includes ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/ispc_texcomp)
  list(APPEND tex_deps 3rdPartyLibs.convert.ispc_texcomp)
endif()
dabuild_plugin(texExp texExp.cpp)
target_include_directories(texExp PRIVATE ${tex_includes})
target_compile_definitions(texExp PRIVATE ${tex_defines})
target_link_libraries(texExp PRIVATE ${tex_deps})
find_package(Astcenc REQUIRED)
target_link_libraries(texExp PRIVATE Astcenc::Astcenc)
