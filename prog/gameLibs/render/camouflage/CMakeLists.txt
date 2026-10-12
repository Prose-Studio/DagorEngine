set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(SourceES camouflageOverrideParamsES.cpp.inl)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.render.camouflage)
target_include_directories(gameLibs.render.camouflage PRIVATE ${includes})
target_link_libraries(gameLibs.render.camouflage PRIVATE Dagor::Quirrel)
dagor_target_es_sources(gameLibs.render.camouflage ${es_sources})
