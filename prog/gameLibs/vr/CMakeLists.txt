dagor_add_target(NAME gameLibs.vr STATIC
  FILES_CMAKE vr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
