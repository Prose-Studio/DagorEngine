set(AllSrcFolder_ES )
dagor_add_dng_module(NAME daNetGameLibs.light_flicker DAS
  FILES_CMAKE light_flicker_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/daNetGameLibs
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
    ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
)
