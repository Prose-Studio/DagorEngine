dagor_add_target(NAME gameLibs.pathFinder.tileCache.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/DetourTileCache/Include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.recastnavigation.Detour 3rdPartyLibs.recastnavigation.DetourTileCache
)
