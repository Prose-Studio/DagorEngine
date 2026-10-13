set(AllSrcFolder_DAS )
dagor_add_dng_module(NAME daNetGameLibs.object_motion_blur
  FILES_CMAKE object_motion_blur_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
