# The reference providers of daBuild (plugins): the assets referenced by composites, effects and splines
include(../dabuildPlugin.cmake)
foreach(provider composit efx spline)
  dabuild_plugin(${provider}RefProv ${provider}RefProv.cpp)
  target_include_directories(${provider}RefProv PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include)
  target_link_libraries(${provider}RefProv PRIVATE engine.startup tools.libTools.assetMgr)
endforeach()
