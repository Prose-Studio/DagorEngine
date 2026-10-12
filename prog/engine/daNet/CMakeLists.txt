# daNet: the ENet based network transport
add_subdirectory(delta)
if(DAGOR_ENGINE_TESTS)
  add_subdirectory(tests)
endif()

set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng ${DAGOR_PROG_DIR}/3rdPartyLibs/enet/include)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
set(deps 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.enet)
if(WIN32)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/posix/include/win32)
  list(APPEND deps 3rdPartyLibs.posix)
endif()

dagor_add_library(engine.daNet ${sources})
target_include_directories(engine.daNet PRIVATE ${includes})
target_link_libraries(engine.daNet PRIVATE ${deps})
