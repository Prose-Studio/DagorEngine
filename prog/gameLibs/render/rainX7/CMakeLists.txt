dagor_add_target(NAME gameLibs.render.rainX7 STATIC
  FILES_CMAKE rainX7_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
