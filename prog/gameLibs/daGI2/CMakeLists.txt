set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR} shaders)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
list(APPEND deps engine.lib3d gameLibs.daSDF)

dagor_add_library(gameLibs.daGI2 ${sources})
target_include_directories(gameLibs.daGI2 PRIVATE ${includes})
target_link_libraries(gameLibs.daGI2 PRIVATE ${deps})
