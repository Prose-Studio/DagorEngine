# The null 3d driver: the driver interface doing nothing at all (command-line tools that only need the API). In trees
# with the multi-driver interface it is one of its drivers, so it has to be in DAGOR_D3D_DRIVERS there.
if(DAGOR_D3D_MULTI)
  if(NOT "null" IN_LIST DAGOR_D3D_DRIVERS)
    message(FATAL_ERROR "engine/drv/drv3d_null in a multi-driver tree needs null in DAGOR_D3D_DRIVERS")
  endif()
endif()
dagor_add_target(NAME engine.drv.drv3d_null STATIC LAX
  FILES_CMAKE drv3d_null_files.cmake
  COMPILE_DEFINITIONS PRIVATE INSIDE_DRIVER
)
