dagor_add_target(NAME gameLibs.gamePhys.phys.destrRenderStub STATIC
  FILES_CMAKE destrRenderStub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
