# Data cache: the file backend
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(deps 3rdPartyLibs.eastl gameLibs.datacache.common)
set(sources filebackend.cpp fileentry.cpp fileutil.cpp)

dagor_add_library(gameLibs.datacache.file ${sources})
target_include_directories(gameLibs.datacache.file PRIVATE ${includes})
target_link_libraries(gameLibs.datacache.file PRIVATE ${deps})
