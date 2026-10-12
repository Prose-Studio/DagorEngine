set(includes
  ${DAGOR_PROG_DIR}/engine/dagorInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
)
set(SourceES outlineRendererCommonES.cpp.inl)
set(sources dasModules/outline.cpp)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.render.outline ${sources})
target_include_directories(gameLibs.render.outline PRIVATE ${includes})
dagor_target_es_sources(gameLibs.render.outline ${es_sources})
