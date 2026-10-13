# The exporters of daBuild, one plugin per asset type: animations (a2dExp), anim chars, collision, fast physics, effects,
# impostors, land classes, local shaders, materials, models (rendinsts, dynamic models, skeletons, grass), physics
# objects and textures.
include(../dabuildPlugin.cmake)
set(shared ${DAGOR_PROG_DIR}/tools/sharedInclude)
set(editor ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include)
set(images 3rdPartyLibs.image.avif 3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.image.psdRead 3rdPartyLibs.image.tiff-4.4.0
  3rdPartyLibs.image.libpng-1.4.22 3rdPartyLibs.arc.zlib-ng)

# a game's asset manager (DAGOR_GAME_ASSET_MANAGER): every exporter in one static library, without the optional ones
# (vehicles, ship sections, APEX destruction), whose pulls are defined empty
if(DAGOR_GAME_ASSET_MANAGER)
  file(CONFIGURE OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/optionalExporters.cpp"
    CONTENT "int pull_vehicle = 0;\nint pull_shipSections = 0;\nint pull_apex = 0;\n")
  find_package(Astcenc REQUIRED)
  dagor_add_target(NAME tools.sceneTools.assetExp.exporters STATIC LAX
    FILES_CMAKE exporters_files.cmake
    INCLUDE_DIRECTORIES PRIVATE
      ${shared} ${editor} ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/nvtt-2.0.7 ${DAGOR_PROG_DIR}/engine/sharedInclude
      ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/math/vhacd
      ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/ispc_texcomp
    COMPILE_DEFINITIONS PRIVATE _TARGET_EXPORTERS_STATIC
    BUILD_DEPENDENCIES PRIVATE
      engine.startup engine.math engine.lib3d engine.shaders engine.perfMon engine.image engine.gameRes engine.scene
      engine.coreUtil engine.consoleProc tools.libTools.assetMgr tools.libTools.assetMgrHlp.emb
      tools.libTools.shaderResBuilder tools.libTools.dagFileRW tools.libTools.util tools.libTools.ambientOcclusion
      tools.libTools.pageAsg tools.libTools.fastPhysData tools.libTools.math tools.libTools.collision
      tools.sceneTools.daEditorX.services.bitMaskMgr tools.sceneTools.assetExp.exporters.scriptHelpersLt
      commonFx.commonFxTools.emb 3rdPartyLibs.math.srcc_msu 3rdPartyLibs.convert.nvtt-2.0.7 ${images}
      3rdPartyLibs.math.vhacd 3rdPartyLibs.convert.ispc_texcomp 3rdPartyLibs.eastl Astcenc::Astcenc
  )
  target_sources(tools.sceneTools.assetExp.exporters PRIVATE "${CMAKE_CURRENT_BINARY_DIR}/optionalExporters.cpp")
  return()
endif()

dabuild_plugin(NAME a2dExp
  FILES_CMAKE a2dExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared} ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes
  BUILD_DEPENDENCIES PRIVATE
    engine.startup tools.libTools.assetMgr engine.math engine.lib3d engine.drv.drv3d_null
    tools.libTools.shaderResBuilder tools.libTools.dagFileRW
)
dabuild_plugin(NAME animCharExp
  FILES_CMAKE animCharExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared}
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math engine.perfMon tools.libTools.assetMgr tools.libTools.pageAsg engine.lib3d engine.shaders
    engine.gameRes engine.scene engine.drv.drv3d_null tools.libTools.shaderResBuilder tools.libTools.dagFileRW
    tools.libTools.ambientOcclusion
)
dabuild_plugin(NAME collisionExp
  FILES_CMAKE collisionExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${shared} ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/math/vhacd
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math engine.lib3d engine.drv.drv3d_null engine.gameRes engine.scene engine.coreUtil
    tools.libTools.assetMgr tools.libTools.dagFileRW tools.libTools.math tools.libTools.collision
    3rdPartyLibs.math.vhacd
)
dabuild_plugin(NAME fastPhysExp
  FILES_CMAKE fastPhysExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared}
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math engine.perfMon tools.libTools.assetMgr tools.libTools.fastPhysData
    tools.libTools.dagFileRW
)
dabuild_plugin(NAME fxExp
  FILES_CMAKE fxExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared}
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math engine.lib3d engine.drv.drv3d_null engine.consoleProc tools.libTools.assetMgr
    tools.libTools.dagFileRW tools.sceneTools.assetExp.exporters.scriptHelpersLt commonFx.commonFxTools
    3rdPartyLibs.math.srcc_msu
)
dabuild_plugin(NAME impostorExp
  FILES_CMAKE impostorExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared} ${editor}
  BUILD_DEPENDENCIES PRIVATE engine.startup tools.libTools.assetMgr
)
dabuild_plugin(NAME landClsExp
  FILES_CMAKE landClsExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared} ${editor}
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.image 3rdPartyLibs.hash tools.libTools.assetMgr tools.sceneTools.daEditorX.services.bitMaskMgr
)
dabuild_plugin(NAME locShadersExp
  FILES_CMAKE locShadersExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared}
  BUILD_DEPENDENCIES PRIVATE engine.startup engine.math tools.libTools.assetMgr
)
dabuild_plugin(NAME matExp
  FILES_CMAKE matExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared}
  BUILD_DEPENDENCIES PRIVATE engine.startup engine.math engine.lib3d tools.libTools.assetMgr tools.libTools.dagFileRW
)
dabuild_plugin(NAME modelExp
  FILES_CMAKE modelExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared} ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_DEFINITIONS PRIVATE _DEBUG_TAB_
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math engine.lib3d engine.shaders engine.drv.drv3d_null engine.gameRes engine.scene
    engine.perfMon tools.libTools.assetMgr tools.libTools.shaderResBuilder tools.libTools.dagFileRW engine.image
    tools.libTools.ambientOcclusion ${images}
)
dabuild_plugin(NAME phObjExp
  FILES_CMAKE phObjExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${shared}
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math engine.lib3d engine.drv.drv3d_null tools.libTools.assetMgr tools.libTools.dagFileRW
)
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
dabuild_plugin(NAME texExp
  FILES_CMAKE texExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${tex_includes}
  COMPILE_DEFINITIONS PRIVATE ${tex_defines}
  BUILD_DEPENDENCIES PRIVATE ${tex_deps}
)
find_package(Astcenc REQUIRED)
target_link_libraries(texExp PRIVATE Astcenc::Astcenc)
