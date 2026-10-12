set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
)
set(sources sqDebugger.cpp scriptProfiler.cpp)

dagor_add_library(gameLibs.quirrel.sqDebugger ${sources})
target_include_directories(gameLibs.quirrel.sqDebugger PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.sqDebugger PRIVATE Dagor::Quirrel)
