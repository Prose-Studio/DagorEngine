# The reference providers of daBuild (plugins): the assets referenced by composites, effects and splines
# (in a game's asset manager, DAGOR_GAME_ASSET_MANAGER, one static library)
if(DAGOR_GAME_ASSET_MANAGER)
  dagor_add_target(NAME tools.sceneTools.assetExp.refProviders STATIC LAX
    FILES_CMAKE refProviders_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    BUILD_DEPENDENCIES PRIVATE engine.startup tools.libTools.assetMgr
  )
  return()
endif()
include(../dabuildPlugin.cmake)
foreach(provider composit efx spline)
  dabuild_plugin(NAME ${provider}RefProv
    FILES_CMAKE ${provider}RefProv_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    BUILD_DEPENDENCIES PRIVATE engine.startup tools.libTools.assetMgr
  )
endforeach()
