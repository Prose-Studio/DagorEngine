dagor_add_target(NAME gameLibs.eventLog STATIC
  FILES_CMAKE eventLog_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
    ${DAGOR_PROG_DIR}/1stPartyLibs/sysinfo
  BUILD_DEPENDENCIES PRIVATE
    1stPartyLibs.jsoncpp 1stPartyLibs.sysinfo gameLibs.asyncHTTPClient gameLibs.asyncResolveAddr
)
