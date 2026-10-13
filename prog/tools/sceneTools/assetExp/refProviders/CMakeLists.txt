# The reference providers of daBuild (plugins): the assets referenced by composites, effects and splines
include(../dabuildPlugin.cmake)
foreach(provider composit efx spline)
  dabuild_plugin(NAME ${provider}RefProv
    FILES_CMAKE ${provider}RefProv_files.cmake
    INCLUDE_DIRECTORIES PRIVATE
      ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    BUILD_DEPENDENCIES PRIVATE engine.startup tools.libTools.assetMgr
  )
endforeach()
