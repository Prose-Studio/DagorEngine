# Data cache: the file backend
dagor_add_target(NAME gameLibs.datacache.file STATIC
  FILES_CMAKE file_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl gameLibs.datacache.common
)
