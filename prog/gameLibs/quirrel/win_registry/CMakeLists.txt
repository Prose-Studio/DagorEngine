# Quirrel bindings of the Windows registry (value reads and writes)
dagor_add_target(NAME gameLibs.quirrel.win_registry STATIC
  FILES_CMAKE win_registry_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
