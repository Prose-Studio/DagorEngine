# HTTP streaming of files
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/ska_hash_map)
set(deps gameLibs.asyncHTTPClient 3rdPartyLibs.eastl)
set(sources http.cpp getdate.cpp)
list(APPEND defines CURL_STATICLIB)

dagor_add_library(gameLibs.streamIO ${sources})
target_include_directories(gameLibs.streamIO PRIVATE ${includes})
target_compile_definitions(gameLibs.streamIO PRIVATE ${defines})
target_link_libraries(gameLibs.streamIO PRIVATE ${deps})
