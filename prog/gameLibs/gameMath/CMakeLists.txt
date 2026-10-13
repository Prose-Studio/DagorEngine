# Game math helpers: convex construction and segments, interpolation tables from BLK, collision node distances
dagor_add_target(NAME gameLibs.gameMath STATIC
  FILES_CMAKE gameMath_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/
)
