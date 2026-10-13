dagor_add_dng_module(NAME daNetGameLibs.collimator_moa DAS
  FILES_CMAKE collimator_moa_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
)
