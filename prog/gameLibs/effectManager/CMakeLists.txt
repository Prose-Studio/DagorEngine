dagor_add_target(NAME gameLibs.effectManager STATIC
  FILES_CMAKE effectManager_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/commonFx/commonFxGame
)
