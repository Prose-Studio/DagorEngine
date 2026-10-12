dagor_add_target(NAME gameLibs.render.wakePs STATIC
  FILES_CMAKE wakePs_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
