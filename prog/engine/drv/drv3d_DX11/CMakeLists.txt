# The Direct3D 11 driver (Windows), with NVAPI, AMD's ADL and DX extensions when their SDKs are there, and Aftermath
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode)
set(defines INSIDE_DRIVER)
set(deps engine/drv/drv3d_commonCode engine/drv/shadersMetaData/dx11)
dagor_require_sdk(nvapi OPTIONAL)
if(TARGET sdk::nvapi)
  list(APPEND deps sdk::nvapi)
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
  dagor_require_sdk(aftermath)
  list(APPEND deps sdk::aftermath)
endif()

dagor_add_library(
  SOURCES
    init.cpp
    drvmain.cpp
    states.cpp
    rtarget.cpp
    texture.cpp
    shaders.cpp
    buffers.cpp
    sampler.cpp
    genericBuffer.cpp
    init_d3di.cpp
    basetex.cpp
    immediateConst.cpp
    helpers.cpp
    memory_metrics.cpp
    clear.cpp
  PRIVATE_INCLUDES ${includes}
  PRIVATE_DEFINES ${defines}
  FORCE_INCLUDES d3d_config.h
  DEPS ${deps}
  SYSTEM_LIBS Version
)
