# Game resources: the resource packs (grp), their descriptions and loading, the factories of the resource types
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-undefined-bool-conversion)
endif()

dagor_add_target(NAME engine.gameRes STATIC
  FILES_CMAKE gameRes_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl engine.daBVH
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
