# daECS loading of entities and templates from DataBlock
list(APPEND deps engine.daECS.utility)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.ioSys)
endif()

dagor_add_target(NAME engine.daECS.io.datablock STATIC
  FILES_CMAKE datablock_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
