add_subdirectory(stub)

dagor_add_target(NAME gameLibs.webui.websocket STATIC
  FILES_CMAKE websocket_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/dagorInclude ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.mongoose
)
