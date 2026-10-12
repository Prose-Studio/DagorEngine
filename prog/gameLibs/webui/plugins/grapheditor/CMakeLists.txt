dagor_add_target(NAME gameLibs.webui.plugins.grapheditor STATIC
  FILES_CMAKE grapheditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude
)
