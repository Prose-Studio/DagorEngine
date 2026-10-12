# daECS loading of entities and templates from DataBlock
set(sources dataBlockReader.cpp)
list(APPEND deps engine.daECS.utility)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.ioSys)
endif()

dagor_add_library(engine.daECS.io.datablock ${sources})
target_link_libraries(engine.daECS.io.datablock PRIVATE ${deps})
