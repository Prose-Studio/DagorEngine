# The 3d driver of the tree's programs (DAGOR_D3D_DRIVERS): the single driver itself, or, with several drivers (or
# DAGOR_D3D_MULTI_FORCED), the multi-driver interface that picks one at run time
set(driver_deps ${DAGOR_D3D_DRIVERS})
list(TRANSFORM driver_deps PREPEND engine.drv.drv3d_)
if(NOT DAGOR_D3D_MULTI)
  dagor_add_target(NAME engine.drv.drv3d_pc_multi HEADERONLY BUILD_DEPENDENCIES INTERFACE ${driver_deps})
  return()
endif()

set(defines INSIDE_DRIVER)
foreach(driver IN LISTS DAGOR_D3D_DRIVERS)
  list(APPEND defines USE_MULTI_D3D_${driver})
endforeach()
dagor_add_target(NAME engine.drv.drv3d_pc_multi STATIC
  FILES_CMAKE drv3d_pc_multi_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE engine.drv.drv3d_commonCode ${driver_deps}
)
