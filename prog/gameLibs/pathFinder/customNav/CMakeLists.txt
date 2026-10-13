dagor_add_target(NAME gameLibs.pathFinder.customNav STATIC
  FILES_CMAKE customNav_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.recastnavigation.Detour
)
