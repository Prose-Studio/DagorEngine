# Data cache: the file backend
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

dagor_add_target(NAME gameLibs.datacache.file STATIC
  FILES_CMAKE file_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl gameLibs.datacache.common
)
