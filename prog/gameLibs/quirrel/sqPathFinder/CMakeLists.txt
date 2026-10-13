dagor_add_target(NAME gameLibs.quirrel.sqPathFinder STATIC
  FILES_CMAKE sqPathFinder_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
