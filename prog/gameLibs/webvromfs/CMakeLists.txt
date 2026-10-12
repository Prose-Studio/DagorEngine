set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(deps gameLibs.datacache)
set(sources webvromfs.cpp)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)

dagor_add_library(gameLibs.webvromfs ${sources})
target_include_directories(gameLibs.webvromfs PRIVATE ${includes})
target_link_libraries(gameLibs.webvromfs PRIVATE ${deps})
