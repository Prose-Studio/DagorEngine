dagor_add_target(NAME gameLibs.gamePhys.collision.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
