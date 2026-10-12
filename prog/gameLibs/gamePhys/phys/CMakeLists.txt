dagor_add_target(NAME gameLibs.gamePhys.phys STATIC
  FILES_CMAKE phys_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
