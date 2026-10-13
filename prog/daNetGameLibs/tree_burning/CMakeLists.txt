dagor_add_dng_module(NAME daNetGameLibs.tree_burning
  FILES_CMAKE tree_burning_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/daNetGameLibs
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
