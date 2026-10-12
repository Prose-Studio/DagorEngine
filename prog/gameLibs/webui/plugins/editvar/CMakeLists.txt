dagor_add_target(NAME gameLibs.webui.plugins.editvar STATIC
  FILES_CMAKE editvar_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude
)
