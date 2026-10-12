set(includes ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include)
set(sources replay.cpp stubs.cpp)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.ioSys)
endif()

dagor_add_library(engine.daECS.net.replay ${sources})
target_include_directories(engine.daECS.net.replay PRIVATE ${includes})
target_link_libraries(engine.daECS.net.replay PRIVATE ${deps})
