add_subdirectory(dasevents)

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND deps 3rdPartyLibs.eastl)
file(GLOB AllSourcesES RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp.inl")
set(SourceES ${AllSourcesES})
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.net)
target_include_directories(gameLibs.ecs.net PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.net PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.net ${es_sources})
