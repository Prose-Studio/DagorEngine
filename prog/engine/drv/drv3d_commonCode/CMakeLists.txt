# Code the 3d drivers share: GPU and display info, base textures, the resource checker, vendor integrations (NVAPI,
# AMD anti-lag and FSR, Streamline), hang handling
set(drivers ${DAGOR_D3D_DRIVERS})
set(sources
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
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode)
set(defines)
if(DAGOR_D3D_MULTI AND drivers STREQUAL "stub")
  list(APPEND defines D3D_STUB_DRIVER_ONLY)
endif()
if(WIN32)
  list(APPEND sources winapi_helpers.cpp)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND sources gpuMemM.mm macosx/macWnd.mm)
endif()
if(APPLE)
  list(APPEND sources displayM.mm)
endif()

find_package(NVAPI)
if(NVAPI_FOUND)
  list(APPEND sources nvLowLatency.cpp)
  list(APPEND deps NVAPI::NVAPI)
else()
  list(APPEND sources nvLowLatencyStub.cpp)
endif()

set(real_drivers ${drivers})
list(REMOVE_ITEM real_drivers stub null)
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64" AND real_drivers)
  list(APPEND sources amdLowLatency.cpp)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/AntiLag2)
else()
  list(APPEND sources amdLowLatencyStub.cpp)
endif()
if(DAGOR_STREAMLINE)
  find_package(Streamline REQUIRED)
  list(APPEND sources streamline_adapter.cpp)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include)
  list(APPEND defines HAS_STREAMLINE)
  list(APPEND deps Streamline::Streamline)
else()
  list(APPEND sources streamline_adapter_stub.cpp)
endif()
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/adl_sdk/include ${DAGOR_PROG_DIR}/3rdPartyLibs/AmdDxExt)
  list(APPEND defines HAS_ADL HAS_AMD_DX_EXT)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$" AND real_drivers AND NOT DAGOR_DEDICATED)
  list(APPEND sources amdFsr.cpp)
  if("vulkan" IN_LIST drivers AND DAGOR_ARCH STREQUAL "x86_64")
    set_property(SOURCE amdFsr.cpp APPEND PROPERTY COMPILE_OPTIONS -DAMDFSR_HAS_VULKAN)
  endif()
  if("DX12" IN_LIST drivers AND DAGOR_ARCH STREQUAL "x86_64")
    set_property(SOURCE amdFsr.cpp APPEND PROPERTY COMPILE_OPTIONS -DAMDFSR_HAS_DX12)
  endif()
else()
  list(APPEND sources amdFsr_stub.cpp)
endif()

dagor_add_library(engine.drv.drv3d_commonCode LAX ${sources})
target_include_directories(engine.drv.drv3d_commonCode PRIVATE ${includes})
target_compile_definitions(engine.drv.drv3d_commonCode PRIVATE ${defines})
target_link_libraries(engine.drv.drv3d_commonCode PRIVATE engine.drv.shadersMetaData)
