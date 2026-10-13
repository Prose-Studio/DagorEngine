# The vehicle exporter of daBuild (a plugin): the vehicle physics assets
include(${DAGOR_PROG_DIR}/tools/sceneTools/assetExp/dabuildPlugin.cmake)
dabuild_plugin(NAME vehicleExp
  FILES_CMAKE exporters_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
  BUILD_DEPENDENCIES PRIVATE engine.startup engine.math tools.libTools.assetMgr
)
