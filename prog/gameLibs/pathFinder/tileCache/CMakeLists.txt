dagor_add_target(NAME gameLibs.pathFinder.tileCache STATIC
  FILES_CMAKE tileCache_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/DetourTileCache/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Recast/Include
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.recastnavigation.Detour 3rdPartyLibs.recastnavigation.DetourTileCache
    3rdPartyLibs.recastnavigation.Recast gameLibs.recastTools Dagor::Phys
)
