set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources commonLoadingJobMgr.cpp)
list(APPEND es_sources gameResES.cpp.inl)
list(APPEND deps 3rdPartyLibs.eastl)

dagor_add_library(gameLibs.ecs.gameres ${sources})
target_include_directories(gameLibs.ecs.gameres PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.gameres PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.gameres ${es_sources})
