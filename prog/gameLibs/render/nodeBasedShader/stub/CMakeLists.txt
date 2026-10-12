# NodeBasedShader stubs for programs without node based shaders
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources nodeBasedShaderStub.cpp)
set(deps gameLibs.nodeBasedShaderManager.stub)

dagor_add_library(gameLibs.render.nodeBasedShader.stub ${sources})
target_include_directories(gameLibs.render.nodeBasedShader.stub PRIVATE ${includes})
target_link_libraries(gameLibs.render.nodeBasedShader.stub PRIVATE ${deps})
