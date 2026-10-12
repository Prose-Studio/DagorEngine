dagor_add_target(NAME gameLibs.render.resourceSlot STATIC
  FILES_CMAKE resourceSlot_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
