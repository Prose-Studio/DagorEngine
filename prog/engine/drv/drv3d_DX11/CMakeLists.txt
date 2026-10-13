# The Direct3D 11 driver (Windows), with NVAPI, AMD's ADL and DX extensions when their SDKs are there, and Aftermath
set(includes ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode)
set(defines INSIDE_DRIVER)
set(deps engine.drv.drv3d_commonCode engine.drv.shadersMetaData.dx11)
find_package(NVAPI)
if(TARGET NVAPI::NVAPI)
  list(APPEND deps NVAPI::NVAPI)
endif()
if(DAGOR_ARCH STREQUAL "x86_64")
  if(IS_DIRECTORY "${DAGOR_PROG_DIR}/3rdPartyLibs/adl_sdk")
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/adl_sdk/include)
    list(APPEND defines HAS_ADL)
  endif()
  if(IS_DIRECTORY "${DAGOR_PROG_DIR}/3rdPartyLibs/AmdDxExt")
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/AmdDxExt)
    list(APPEND defines HAS_AMD_DX_EXT)
  endif()
  find_package(Aftermath REQUIRED)
  list(APPEND deps Aftermath::Aftermath)
endif()

dagor_add_target(NAME engine.drv.drv3d_DX11 STATIC LAX
  FILES_CMAKE drv3d_DX11_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES
    PUBLIC System::version
    PRIVATE ${deps}
  FORCE_INCLUDES d3d_config.h
)
