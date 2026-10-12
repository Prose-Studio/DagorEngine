set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(SourceES smokeOccluderES.cpp.inl)
list(APPEND es_sources ${SourceES})
list(APPEND deps engine.daECS.core)

dagor_add_library(gameLibs.smokeOccluder)
target_include_directories(gameLibs.smokeOccluder PRIVATE ${includes})
target_link_libraries(gameLibs.smokeOccluder PRIVATE ${deps})
dagor_target_es_sources(gameLibs.smokeOccluder ${es_sources})
