list(APPEND deps engine.lib3d gameLibs.resourcePool)
if(DAGOR_GAME_RENDERER)
  list(APPEND deps gameLibs.render.nodeBasedShader)
else()
  list(APPEND deps gameLibs.render.nodeBasedShader.stub)
endif()

dagor_add_target(NAME gameLibs.daSkies2 STATIC
  FILES_CMAKE daSkies2_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR} shaders
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
