if(DAGOR_BUILDING_TOOLS)
  set(defines _TARGET_PC_TOOLS_BUILD)
endif()

dagor_add_target(NAME gameLibs.pathFinder STATIC
  FILES_CMAKE pathFinder_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/DetourTileCache/Include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.recastnavigation.Detour 3rdPartyLibs.recastnavigation.DetourTileCache 3rdPartyLibs.arc.zstd-1.4.5
    gameLibs.gameMath gameLibs.recastTools
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
