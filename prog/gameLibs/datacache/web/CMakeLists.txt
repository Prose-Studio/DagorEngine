# Data cache: the web (HTTP) backend
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(deps 3rdPartyLibs.eastl gameLibs.datacache.common gameLibs.datacache.file gameLibs.streamIO)
set(sources webbackend.cpp webindex.cpp webutil.cpp gzip.cpp)
list(APPEND defines OPENSSL_SUPPRESS_DEPRECATED)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)

dagor_add_library(gameLibs.datacache.web ${sources})
target_include_directories(gameLibs.datacache.web PRIVATE ${includes})
target_compile_definitions(gameLibs.datacache.web PRIVATE ${defines})
target_link_libraries(gameLibs.datacache.web PRIVATE ${deps})
