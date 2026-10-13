dagor_add_target(NAME gameLibs.sepClientInstance STATIC
  FILES_CMAKE sepClientInstance_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  BUILD_DEPENDENCIES PRIVATE gameLibs.sepClient
)
