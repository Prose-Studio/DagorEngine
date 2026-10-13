dagor_add_target(NAME gameLibs.covers STATIC
  FILES_CMAKE covers_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.recastnavigation.Detour engine.scene
)
