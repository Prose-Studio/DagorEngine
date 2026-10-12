dagor_add_target(NAME gameLibs.daPhys STATIC
  FILES_CMAKE daPhys_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.regExp
)
