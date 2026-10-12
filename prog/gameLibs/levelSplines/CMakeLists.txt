dagor_add_target(NAME gameLibs.levelSplines STATIC LAX
  FILES_CMAKE levelSplines_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
