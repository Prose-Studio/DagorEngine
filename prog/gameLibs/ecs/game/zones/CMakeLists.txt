set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(SourceES )
dagor_glob_sources(SourceES DIRS . GLOB *ES.cpp.inl)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.game.zones)
target_include_directories(gameLibs.ecs.game.zones PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.game.zones PRIVATE Dagor::Quirrel)
dagor_target_es_sources(gameLibs.ecs.game.zones ${es_sources})
