dagor_add_dng_module(NAME daNetGameLibs.blood_puddles DAS
  FILES_CMAKE blood_puddles_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
