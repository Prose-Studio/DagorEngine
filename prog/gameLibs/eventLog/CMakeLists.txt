set(sources dataHelpers.cpp eventLog.cpp errorLog.cpp httpRequest.cpp)
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/sysinfo
)
list(APPEND deps 1stPartyLibs.jsoncpp 1stPartyLibs.sysinfo gameLibs.asyncHTTPClient gameLibs.asyncResolveAddr)

dagor_add_library(gameLibs.eventLog ${sources})
target_include_directories(gameLibs.eventLog PRIVATE ${includes})
target_link_libraries(gameLibs.eventLog PRIVATE ${deps})
