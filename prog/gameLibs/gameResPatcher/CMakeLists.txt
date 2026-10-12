# Patching of game resource packs (GRP/DxP), vromfs packs and sound banks, reusing unchanged data
dagor_add_target(NAME gameLibs.gameResPatcher STATIC LAX
  FILES_CMAKE gameResPatcher_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine
)
