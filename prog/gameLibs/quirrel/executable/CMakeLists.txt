dagor_add_target(NAME gameLibs.quirrel.executable STATIC
  FILES_CMAKE executable_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
