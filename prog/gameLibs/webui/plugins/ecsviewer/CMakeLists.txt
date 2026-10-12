dagor_add_target(NAME gameLibs.webui.plugins.ecsviewer STATIC
  FILES_CMAKE ecsviewer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/dagorInclude
)
