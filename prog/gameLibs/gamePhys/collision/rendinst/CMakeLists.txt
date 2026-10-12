dagor_add_target(NAME gameLibs.gamePhys.collision.rendinst STATIC
  FILES_CMAKE rendinst_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
