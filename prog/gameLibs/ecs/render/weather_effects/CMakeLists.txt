set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND deps 3rdPartyLibs.eastl)
set(SourceES lightningES.cpp.inl)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.render.weather_effects)
target_include_directories(gameLibs.ecs.render.weather_effects PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.render.weather_effects PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.render.weather_effects ${es_sources})
