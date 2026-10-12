# Data cache: shared tracing
set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude)
set(sources trace.cpp)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.kernel)
endif()

dagor_add_library(gameLibs.datacache.common ${sources})
target_include_directories(gameLibs.datacache.common PRIVATE ${includes})
target_link_libraries(gameLibs.datacache.common PRIVATE ${deps})
