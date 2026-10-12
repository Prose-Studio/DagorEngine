dagor_add_dng_module(NAME daNetGameLibs.blurred_ui
  FILES_CMAKE blurred_ui_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
