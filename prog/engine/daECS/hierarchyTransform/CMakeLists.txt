list(APPEND deps 3rdPartyLibs.eastl)
set(SourceES hierarchyTransformES.cpp.inl)
list(APPEND es_sources ${SourceES})

dagor_add_library(engine.daECS.hierarchyTransform)
target_link_libraries(engine.daECS.hierarchyTransform PRIVATE ${deps})
dagor_target_es_sources(engine.daECS.hierarchyTransform ${es_sources})
