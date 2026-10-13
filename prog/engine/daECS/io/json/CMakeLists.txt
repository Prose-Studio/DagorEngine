dagor_add_target(NAME engine.daECS.io.json STATIC
  FILES_CMAKE json_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.jsoncpp 3rdPartyLibs.eastl engine.daECS.core
)
