add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources riexSyncNet.cpp)
list(APPEND deps 3rdPartyLibs.eastl gameLibs.rendInst)
set(SourceES )
dagor_glob_sources(SourceES DIRS . GLOB *ES.cpp.inl)
list(APPEND deps Dagor::Phys)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.rendInst ${sources})
target_include_directories(gameLibs.ecs.rendInst PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.rendInst PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.rendInst ${es_sources})
