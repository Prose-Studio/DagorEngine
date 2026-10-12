dagor_add_target(NAME gameLibs.webui.plugins.quirrel STATIC
  FILES_CMAKE quirrel_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/dagorInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
