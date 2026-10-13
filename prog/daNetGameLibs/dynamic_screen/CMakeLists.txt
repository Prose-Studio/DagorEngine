dagor_add_dng_module(NAME daNetGameLibs.dynamic_screen
  FILES_CMAKE dynamic_screen_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
