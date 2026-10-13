# the swimming splashes, on the tree's physics (Dagor::Phys)
dagor_add_dng_module(NAME daNetGameLibs.swim_splash
  FILES_CMAKE swim_splash_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
