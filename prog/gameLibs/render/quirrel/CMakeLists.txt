dagor_add_target(NAME gameLibs.render.quirrel STATIC
  FILES_CMAKE quirrel_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel gameLibs.quirrel.bindQuirrelEx
)
