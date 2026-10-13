dagor_add_dng_module(NAME gameLibs.route_prober DAS
  FILES_CMAKE route_prober_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
)
