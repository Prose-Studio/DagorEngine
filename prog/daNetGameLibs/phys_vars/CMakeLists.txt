dagor_add_dng_module(NAME daNetGameLibs.phys_vars DAS
  FILES_CMAKE phys_vars_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
