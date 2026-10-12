add_subdirectory(stub)

set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/3rdPartyLibs/pcre/pcre
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
set(sources
  actionData.cpp
  actionsAndBindings.cpp
  actionProcessing.cpp
  userConfig.cpp
  actionSqBind.cpp
  dargSqBind.cpp
  actionsDbg.cpp
)
list(APPEND deps 3rdPartyLibs.eastl)

dagor_add_library(gameLibs.daInput ${sources})
target_include_directories(gameLibs.daInput PRIVATE ${includes})
target_link_libraries(gameLibs.daInput PRIVATE Dagor::Quirrel ${deps})
