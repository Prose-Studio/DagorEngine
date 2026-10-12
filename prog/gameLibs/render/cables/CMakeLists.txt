add_subdirectory(stub)

dagor_add_target(NAME gameLibs.render.cables STATIC
  FILES_CMAKE cables_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE engine.lib3d gameLibs.render
)
