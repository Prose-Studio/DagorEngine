dagor_add_target(NAME gameLibs.render.foam STATIC
  FILES_CMAKE foam_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
