set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.screen_vhs
  FILES_CMAKE screen_vhs_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.vhsCameraCommon
)
