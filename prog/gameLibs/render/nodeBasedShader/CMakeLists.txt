add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources nodeBasedShader.cpp)
set(SourceES nodeBasedShaderES.cpp.inl)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.render.nodeBasedShader ${sources})
target_include_directories(gameLibs.render.nodeBasedShader PRIVATE ${includes})
dagor_target_es_sources(gameLibs.render.nodeBasedShader ${es_sources})
