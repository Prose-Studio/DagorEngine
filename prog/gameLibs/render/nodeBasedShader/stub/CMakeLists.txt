# NodeBasedShader stubs for programs without node based shaders
dagor_add_target(NAME gameLibs.render.nodeBasedShader.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE gameLibs.nodeBasedShaderManager.stub
)
