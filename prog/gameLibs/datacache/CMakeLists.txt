add_subdirectory(common)
add_subdirectory(file)
add_subdirectory(web)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources datacache.cpp)
list(APPEND deps gameLibs.datacache.common gameLibs.datacache.file gameLibs.datacache.web)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)

dagor_add_library(gameLibs.datacache ${sources})
target_include_directories(gameLibs.datacache PRIVATE ${includes})
target_link_libraries(gameLibs.datacache PRIVATE ${deps})
