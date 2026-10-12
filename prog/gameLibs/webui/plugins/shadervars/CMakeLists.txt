dagor_add_target(NAME gameLibs.webui.plugins.shadervars STATIC
  FILES_CMAKE shadervars_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/webui ${DAGOR_PROG_DIR}/dagorInclude
)
