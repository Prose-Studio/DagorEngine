dagor_add_target(NAME gameLibs.decalMatrices STATIC
  FILES_CMAKE decalMatrices_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE engine.lib3d
)
