# The Metal driver (macOS, iOS, tvOS); DAGOR_METALFX: MetalFX upscaling (the MetalFX framework)
option(DAGOR_METALFX "Metal: MetalFX upscaling" OFF)
set(defines INSIDE_DRIVER)
set(system_libs System::CoreGraphics) # the color spaces of HDR output
if(DAGOR_METALFX)
  list(APPEND defines USE_METALFX_UPSCALE)
  list(APPEND system_libs System::MetalFX)
endif()

dagor_add_target(NAME engine.drv.drv3d_Metal STATIC LAX
  FILES_CMAKE drv3d_Metal_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES
    PUBLIC ${system_libs}
    PRIVATE engine.drv.drv3d_commonCode 3rdPartyLibs.hash
  FORCE_INCLUDES d3d_config.h
)
