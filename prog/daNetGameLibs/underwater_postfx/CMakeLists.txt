dagor_add_dng_module(NAME daNetGameLibs.underwater_postfx
  FILES_CMAKE underwater_postfx_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/daNetGameLibs
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
)
