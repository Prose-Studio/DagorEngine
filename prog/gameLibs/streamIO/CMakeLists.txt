# HTTP streaming of files
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

dagor_add_target(NAME gameLibs.streamIO STATIC
  FILES_CMAKE streamIO_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/ska_hash_map
  COMPILE_DEFINITIONS PRIVATE CURL_STATICLIB
  BUILD_DEPENDENCIES PRIVATE gameLibs.asyncHTTPClient 3rdPartyLibs.eastl
)
