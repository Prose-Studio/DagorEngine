# The Metal driver (macOS, iOS, tvOS); DAGOR_METALFX: MetalFX upscaling (the MetalFX framework)
option(DAGOR_METALFX "Metal: MetalFX upscaling" OFF)
set(defines INSIDE_DRIVER)
set(system_libs)
if(DAGOR_METALFX)
  list(APPEND defines USE_METALFX_UPSCALE)
  set(system_libs "$<LINK_LIBRARY:FRAMEWORK,MetalFX>")
endif()

dagor_add_library(engine.drv.drv3d_Metal LAX buffers.mm bindless.mm vdecl.mm program.mm shader.mm shadersPreCache.mm
  texture.mm metalview.mm render.mm init_d3di.cpp d3d_buffers.mm d3d_bindless.mm d3d_initialSettings.cpp
  d3d_unimplemented.cpp d3d_shaders.mm d3d_texture.mm d3d_samplers.mm d3d_rtarget.mm d3d_states.mm d3d_tm.mm
  d3d_render_main.mm d3d_raytracing.mm acceleration_structure_desc.mm)
target_include_directories(engine.drv.drv3d_Metal PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode)
target_compile_definitions(engine.drv.drv3d_Metal PRIVATE ${defines})
target_link_libraries(engine.drv.drv3d_Metal PRIVATE engine.drv.drv3d_commonCode 3rdPartyLibs.hash)
target_link_libraries(engine.drv.drv3d_Metal PUBLIC ${system_libs})
dagor_target_force_include(engine.drv.drv3d_Metal d3d_config.h)
