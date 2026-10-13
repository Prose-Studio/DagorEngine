dagor_add_dng_module(NAME daNetGameLibs.billboard_decals DAS
  FILES_CMAKE billboard_decals_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/daNetGameLibs
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
)
