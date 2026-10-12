set(sources scene.cpp)
list(APPEND deps engine.daECS.io.datablock engine.daECS.core 3rdPartyLibs.eastl)

dagor_add_library(engine.daECS.scene ${sources})
target_link_libraries(engine.daECS.scene PRIVATE ${deps})
