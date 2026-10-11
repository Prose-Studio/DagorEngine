# The Direct3D 12 driver (Windows x64 and arm64) on the Agility SDK, with its GPU crash reporting (DRED, AGS, Aftermath),
# the capture tools' integration and the upscalers (FidelityFX FSR on x64; XeSS has its stub: the fork has no
# 3rdPartyLibs/xess_sdk). The programs that link it ship the Agility, AGS and FidelityFX runtime next to them.
if(NOT DAGOR_PLATFORM STREQUAL "windows" OR NOT DAGOR_ARCH MATCHES "^(x86_64|arm64)$")
  message(FATAL_ERROR "drv3d_DX12 is for Windows x64 and arm64, not ${DAGOR_PLATFORM}-${DAGOR_ARCH}")
endif()
set(dev "$<NOT:$<CONFIG:Rel>>")
set(dir ${CMAKE_CURRENT_SOURCE_DIR})
set(sources
  init_d3di.cpp
  dx12.cpp
  enhanced_barrier_validation.cpp
  device.cpp
  device_queue.cpp
  swapchain.cpp
  format_store.cpp
  device_context.cpp
  query_manager.cpp
  synced_command_store.cpp
  mirrored_ring_memory.cpp
  shader.cpp
  texture.cpp
  pipeline.cpp
  pipeline_cache.cpp
  bindless.cpp
  d3d12_error_handling.cpp
  resource_memory_heap.cpp
  resource_manager/heap_components.cpp
  resource_manager/buffer_components.cpp
  resource_manager/buffer_components_heap.cpp
  resource_manager/buffer_components_heap_state.cpp
  resource_manager/buffer_components_heap_suballocator.cpp
  resource_manager/rtx_components.cpp
  resource_manager/host_shared_components.cpp
  resource_update_buffer.cpp
  pipeline/blk_cache.cpp
  ray_trace_pipeline.cpp
  debug/names.cpp
  platform_pc.cpp
  debug/global_state.cpp
  debug/device_state_pc.cpp
  debug/gpu_postmortem_dagor_trace.cpp
  debug/gpu_postmortem_microsoft_dred.cpp
  debug/pipeline_resource_reporter.cpp
  shader_library.cpp
  debug/gpu_capture/generic_tools.cpp
  debug/gpu_capture/legacy_pix.cpp
  debug/gpu_capture/nsight.cpp
  debug/gpu_capture/render_doc.cpp
  # the debug tools outside Rel
  "$<${dev}:${dir}/debug/debug_types.cpp>"
  "$<${dev}:${dir}/debug/frame_command_logger.cpp>"
  "$<${dev}:${dir}/resource_usage_debugger.cpp>"
  xess_wrapper_stub.cpp
)
set(defines INSIDE_DRIVER D3DX12_NO_STATE_OBJECT_HELPERS) # (the state object helpers need WRL)
set(deps engine/drv/drv3d_commonCode engine/drv/shadersMetaData/dxil engine/shaders 1stPartyLibs/jsoncpp)
set(runtime)

# the Agility SDK's d3d12.h comes before the Windows SDK's
dagor_require_sdk(agility)
list(APPEND deps sdk::agility)
dagor_require_sdk(nvapi OPTIONAL)
if(TARGET sdk::nvapi)
  list(APPEND deps sdk::nvapi)
endif()
if(DAGOR_ARCH STREQUAL "x86_64")
  # AMD GPU Services: markers for crash reports, Radeon GPU Profiler captures
  dagor_require_sdk(ags)
  list(APPEND deps sdk::ags)
  list(APPEND sources debug/amd_ags_init.cpp debug/gpu_capture/radeon_gpu_profiler.cpp debug/gpu_postmortem_ags_trace.cpp)
  list(APPEND runtime ${DAGOR_SDK_AGS_RUNTIME})
  dagor_require_sdk(aftermath)
  list(APPEND deps sdk::aftermath)
  list(APPEND sources debug/gpu_postmortem_nvidia_aftermath.cpp)
  # FidelityFX FSR upscaling and frame generation
  dagor_require_sdk(fidelityfx)
  list(APPEND deps sdk::fidelityfx)
  list(APPEND sources amdFsrD3D12_windows.cpp fsr_wrapper.cpp)
  list(APPEND runtime ${DAGOR_SDK_FIDELITYFX_RUNTIME})
else()
  list(APPEND sources fsr_wrapper_stub.cpp)
endif()

dagor_add_library(STRICT
  SOURCES ${sources}
  PRIVATE_INCLUDES
    ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
    ${DAGOR_PROG_DIR}/engine/drv/drv3d_DX12
    ${DAGOR_PROG_DIR}/engine/shaders
    ${DAGOR_PROG_DIR}/dagorInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  PRIVATE_DEFINES ${defines}
  FORCE_INCLUDES d3d_config.h
  DEPS ${deps}
)
# what the programs that link the driver load: D3D12Core and the SDK layers in D3D12/, the vendor libraries next to them
dagor_runtime_files(engine.drv.drv3d_DX12 SUBDIR D3D12 FILES ${DAGOR_SDK_AGILITY_RUNTIME})
if(runtime)
  dagor_runtime_files(engine.drv.drv3d_DX12 FILES ${runtime})
endif()
