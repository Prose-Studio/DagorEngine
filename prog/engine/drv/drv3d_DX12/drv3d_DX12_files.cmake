set(dev "$<NOT:$<CONFIG:Rel>>")
set(dir ${CMAKE_CURRENT_LIST_DIR})
set(FILES
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
if(DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND FILES debug/amd_ags_init.cpp debug/gpu_capture/radeon_gpu_profiler.cpp debug/gpu_postmortem_ags_trace.cpp)
  list(APPEND FILES debug/gpu_postmortem_nvidia_aftermath.cpp)
  list(APPEND FILES amdFsrD3D12_windows.cpp fsr_wrapper.cpp)
else()
  list(APPEND FILES fsr_wrapper_stub.cpp)
endif()
