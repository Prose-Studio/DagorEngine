dagor_add_target(NAME gameLibs.webui.plugins.editorCurves STATIC
  FILES_CMAKE editorCurves_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude
)
