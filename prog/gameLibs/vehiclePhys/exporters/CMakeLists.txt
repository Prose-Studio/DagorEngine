# The vehicle exporter of daBuild (a plugin): the vehicle physics assets
include(${DAGOR_PROG_DIR}/tools/sceneTools/assetExp/dabuildPlugin.cmake)
dabuild_plugin(vehicleExp vehicleExp.cpp)
target_include_directories(vehicleExp PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_link_libraries(vehicleExp PRIVATE engine.startup engine.math tools.libTools.assetMgr)
