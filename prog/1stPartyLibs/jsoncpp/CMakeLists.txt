# jsoncpp on EASTL containers (the engine's variant of 3rdPartyLibs/jsoncpp, whose license it carries)
dagor_add_target(NAME 1stPartyLibs.jsoncpp STATIC LAX
  FILES_CMAKE jsoncpp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
  LICENSES ${DAGOR_PROG_DIR}/3rdPartyLibs/jsoncpp
)
