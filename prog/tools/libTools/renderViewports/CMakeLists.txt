dagor_add_target(NAME tools.libTools.renderViewports STATIC LAX
  FILES_CMAKE renderViewports_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
