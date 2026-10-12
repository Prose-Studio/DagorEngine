# Data cache: shared tracing
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.kernel)
endif()

dagor_add_target(NAME gameLibs.datacache.common STATIC
  FILES_CMAKE common_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
