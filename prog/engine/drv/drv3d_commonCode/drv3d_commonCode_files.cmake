set(FILES
  drvDecl.cpp
  gpuMem.cpp
  gpuVendor.cpp
  gpuConfig.cpp
  display.cpp
  d3dToTexFmt.cpp
  basetexture.cpp
  drv_utils.cpp
  drv_resourceChecker.cpp
  dxgi_utils.cpp
  stereoHelper.cpp
  hangHandler.cpp
  ICrashFallback.cpp
  drv_returnAddrStore.cpp
  resUpdateBufferGeneric.cpp
  resourceActivationGeneric.cpp
  texResizeGeneric.cpp
  destroyEvent.cpp
  gpuLatency.cpp
)
if(NVAPI_FOUND)
  list(APPEND FILES nvLowLatency.cpp)
else()
  list(APPEND FILES nvLowLatencyStub.cpp)
endif()
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64" AND real_drivers)
  list(APPEND FILES amdLowLatency.cpp)
else()
  list(APPEND FILES amdLowLatencyStub.cpp)
endif()
if(DAGOR_STREAMLINE)
  list(APPEND FILES streamline_adapter.cpp)
else()
  list(APPEND FILES streamline_adapter_stub.cpp)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$" AND real_drivers AND NOT DAGOR_DEDICATED)
  list(APPEND FILES amdFsr.cpp)
  if("vulkan" IN_LIST drivers AND DAGOR_ARCH STREQUAL "x86_64")
    set_property(SOURCE amdFsr.cpp APPEND PROPERTY COMPILE_OPTIONS -DAMDFSR_HAS_VULKAN)
  endif()
  if("DX12" IN_LIST drivers AND DAGOR_ARCH STREQUAL "x86_64")
    set_property(SOURCE amdFsr.cpp APPEND PROPERTY COMPILE_OPTIONS -DAMDFSR_HAS_DX12)
  endif()
else()
  list(APPEND FILES amdFsr_stub.cpp)
endif()
