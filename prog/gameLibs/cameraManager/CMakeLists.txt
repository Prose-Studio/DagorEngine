# The camera manager (a gameLibs module, its pull framework_cameraManager_pull): with the renderer only, without it
# games link gameLibs/cameraManager/stub
set(deps)
if(DAGOR_GAME_RENDERER)
  set(deps gameLibs.folders)
endif()
dagor_add_dng_module(NAME gameLibs.cameraManager
  FILES_CMAKE cameraManager_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
