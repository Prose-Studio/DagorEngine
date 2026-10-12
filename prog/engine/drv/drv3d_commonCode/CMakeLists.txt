# Code the 3d drivers share: GPU and display info, base textures, the resource checker, vendor integrations (NVAPI,
# AMD anti-lag and FSR, Streamline), hang handling
set(drivers ${DAGOR_D3D_DRIVERS})
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode)
set(defines)
if(DAGOR_D3D_MULTI AND drivers STREQUAL "stub")
  list(APPEND defines D3D_STUB_DRIVER_ONLY)
endif()

find_package(NVAPI)
if(NVAPI_FOUND)
  list(APPEND deps NVAPI::NVAPI)
endif()

set(real_drivers ${drivers})
list(REMOVE_ITEM real_drivers stub null)
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64" AND real_drivers)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/AntiLag2)
endif()
if(DAGOR_STREAMLINE)
  find_package(Streamline REQUIRED)
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include)
  list(APPEND defines HAS_STREAMLINE)
  list(APPEND deps Streamline::Streamline)
endif()
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/adl_sdk/include ${DAGOR_PROG_DIR}/3rdPartyLibs/AmdDxExt)
  list(APPEND defines HAS_ADL HAS_AMD_DX_EXT)
endif()

dagor_add_target(NAME engine.drv.drv3d_commonCode STATIC LAX
  FILES_CMAKE drv3d_commonCode_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE engine.drv.shadersMetaData
)
