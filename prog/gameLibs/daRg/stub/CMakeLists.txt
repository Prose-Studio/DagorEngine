set(sources daRgStub.cpp)

dagor_add_library(gameLibs.daRg.stub ${sources})
target_link_libraries(gameLibs.daRg.stub PRIVATE Dagor::Quirrel)
