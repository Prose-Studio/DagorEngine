dagor_add_target(NAME gameLibs.asyncResolveAddr STATIC
  FILES_CMAKE asyncResolveAddr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
