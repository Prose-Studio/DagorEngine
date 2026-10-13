dagor_add_target(NAME gameLibs.gamePhys.phys.destrRenderStub STATIC
  FILES_CMAKE destrRenderStub_files.cmake
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
