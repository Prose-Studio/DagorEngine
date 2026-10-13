# Navigation mesh tools on Recast: covers, edges, jump links (the tools build it with the Tab checks)
dagor_add_target(NAME gameLibs.recastTools STATIC
  FILES_CMAKE recastTools_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/DetourTileCache/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Recast/Include ${CMAKE_CURRENT_SOURCE_DIR}
  COMPILE_DEFINITIONS PRIVATE $<$<BOOL:${DAGOR_BUILDING_TOOLS}>:_DEBUG_TAB_>
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.recastnavigation.Detour 3rdPartyLibs.recastnavigation.DetourTileCache
    3rdPartyLibs.recastnavigation.Recast gameLibs.gameMath
)
