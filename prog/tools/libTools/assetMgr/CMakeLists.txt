# The tools asset manager: asset bases and types, assets from game resources and DDSx textures, change tracking
dagor_add_target(NAME tools.libTools.assetMgr STATIC LAX
  FILES_CMAKE assetMgr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
