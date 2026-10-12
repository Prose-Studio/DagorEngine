dagor_add_target(NAME gameLibs.quirrel.ecsComputed STATIC
  FILES_CMAKE ecsComputed_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/gameLibs
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
