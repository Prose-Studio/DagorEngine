# daECS game resource stubs for programs without game resources
set(sources gameResStub.cpp)
list(APPEND deps engine.daECS.core 3rdPartyLibs.eastl)

dagor_add_library(engine.daECS.gameResStub ${sources})
target_link_libraries(engine.daECS.gameResStub PRIVATE ${deps})
