set(includes
  ${DAGOR_PROG_DIR}/engine/dagorInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
)
set(sources deferToActModule.cpp)
list(APPEND deps 3rdPartyLibs.eastl)
file(GLOB AllSourcesES RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp.inl")
set(SourceES ${AllSourcesES})
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.deferToAct ${sources})
target_include_directories(gameLibs.ecs.deferToAct PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.deferToAct PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.deferToAct ${es_sources})
