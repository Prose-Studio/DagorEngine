dagor_add_dng_module(NAME daNetGameLibs.pathfinder DAS
  FILES_CMAKE pathfinder_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/DetourTileCache/Include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.recastnavigation.Detour 3rdPartyLibs.recastnavigation.DetourTileCache gameLibs.pathFinder
    gameLibs.pathFinder.tileCache gameLibs.pathFinder.customNav gameLibs.quirrel.sqPathFinder
    gameLibs.dasModules.pathFinder
  PULL_VARS dng_pathfinder_sq dng_pathfinder_con
)
