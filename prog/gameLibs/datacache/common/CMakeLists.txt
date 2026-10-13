# Data cache: shared tracing
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.kernel)
endif()

dagor_add_target(NAME gameLibs.datacache.common STATIC
  FILES_CMAKE common_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
