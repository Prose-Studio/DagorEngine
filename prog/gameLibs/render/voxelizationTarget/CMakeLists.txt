if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  set(deps engine.baseUtil)
endif()
list(APPEND deps engine.lib3d)

dagor_add_target(NAME gameLibs.render.voxelizationTarget STATIC
  FILES_CMAKE voxelizationTarget_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
