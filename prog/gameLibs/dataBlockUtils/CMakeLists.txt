dagor_add_target(NAME gameLibs.dataBlockUtils STATIC
  FILES_CMAKE dataBlockUtils_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.jsoncpp
)
