set(includes
  ${DAGOR_PROG_DIR}/engine/dagorInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/engine/consoleProc
)
set(sources ecsConsole.cpp)
list(APPEND deps 3rdPartyLibs.eastl)
set(SourceES )
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.console ${sources})
target_include_directories(gameLibs.ecs.console PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.console PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.console ${es_sources})
