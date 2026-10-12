# The 3d driver of the tree's programs (DAGOR_D3D_DRIVERS): the single driver itself, or, with several drivers (or
# DAGOR_D3D_MULTI_FORCED), the multi-driver interface that picks one at run time
set(drivers ${DAGOR_D3D_DRIVERS})
set(driver_deps ${drivers})
list(TRANSFORM driver_deps PREPEND engine.drv.drv3d_)
if(NOT DAGOR_D3D_MULTI)
  dagor_add_library(engine.drv.drv3d_pc_multi INTERFACE)
  target_link_libraries(engine.drv.drv3d_pc_multi INTERFACE ${driver_deps})
  return()
endif()

set(sources init.cpp)
if(WIN32)
  if("DX11" IN_LIST drivers OR "DX12" IN_LIST drivers)
    list(APPEND sources hlsl_dx.cpp)
  else()
    list(APPEND sources hlsl_stub.cpp)
  endif()
endif()
set(defines INSIDE_DRIVER)
foreach(driver IN LISTS drivers)
  list(APPEND defines USE_MULTI_D3D_${driver})
endforeach()

dagor_add_library(engine.drv.drv3d_pc_multi ${sources})
target_include_directories(engine.drv.drv3d_pc_multi PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode)
target_compile_definitions(engine.drv.drv3d_pc_multi PRIVATE ${defines})
target_link_libraries(engine.drv.drv3d_pc_multi PRIVATE engine.drv.drv3d_commonCode ${driver_deps})
