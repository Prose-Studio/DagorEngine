dagor_add_target(NAME gameLibs.webui.plugins.dargMcp STATIC
  FILES_CMAKE dargMcp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel 3rdPartyLibs.image.libpng-1.4.22
)
