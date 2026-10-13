dagor_add_dng_module(NAME daNetGameLibs.static_flares
  FILES_CMAKE static_flares_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
)
