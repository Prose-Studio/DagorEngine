set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
)
set(sources sqSysInfo.cpp)
set(deps gameLibs.userSystemInfo)

dagor_add_library(gameLibs.quirrel.sqSysInfo ${sources})
target_include_directories(gameLibs.quirrel.sqSysInfo PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqSysInfo PRIVATE Dagor::Quirrel ${deps})
