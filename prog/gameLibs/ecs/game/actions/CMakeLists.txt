set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND es_sources actionES.cpp.inl)

dagor_add_library(gameLibs.ecs.game.actions)
target_include_directories(gameLibs.ecs.game.actions PRIVATE ${includes})
dagor_target_es_sources(gameLibs.ecs.game.actions ${es_sources})
