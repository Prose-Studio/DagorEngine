# daFrameGraph unit tests, with mock shader variables. They run on the stub driver (cases that need a GPU skip
# themselves); in trees with a real 3d driver also on that one (gameLibs.daFrameGraph, requires a GPU).
set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  set(options -Wc++11-narrowing -Wswitch -Wbitfield-constant-conversion -Wmissing-field-initializers)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set(options /wd4458) # locals that hide members (jam builds these tests with clang only)
endif()
dagor_add_catch2_test(daFrameGraph-tests TIMEOUT 1200 TAGS gameLibs render ARGS --gpu-driver stub main.cpp benchmark.cpp
  runtime.cpp multiplexing.cpp idContainers.cpp barrierScheduler.cpp cycAlloc.cpp bitSearch.cpp irGraphBuilder.cpp
  nodeStateDeltas.cpp nodeRemap.cpp resourceScheduler.cpp heapLayout.cpp layoutUpdate.cpp heapPolicy.cpp
  layoutOptimizer.cpp virtualPassRequest.cpp refinedBlock.cpp resourceLruCache.cpp resourceLruCacheBenchmark.cpp)
target_include_directories(daFrameGraph-tests PRIVATE .. ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_compile_options(daFrameGraph-tests PRIVATE ${options})
target_link_libraries(daFrameGraph-tests PRIVATE engine.memory engine.kernel engine.osApiWrappers engine.coreUtil
  engine.baseUtil engine.ioSys engine.math engine.shaders engine.lib3d engine.image engine.startup engine.workCycle
  engine.perfMon.stub engine.drv.drv3d_pc_multi engine.osApiWrappers.messageBox 3rdPartyLibs.eastl
  gameLibs.render.daFrameGraph)
set_target_properties(daFrameGraph-tests PROPERTIES DAGOR_SHADER_VARS mock DAGOR_LINUX_GUI ON)
set(real_drivers ${DAGOR_D3D_DRIVERS})
list(REMOVE_ITEM real_drivers stub null)
if(real_drivers)
  dagor_add_catch2_run(daFrameGraph-tests gameLibs.daFrameGraph TAGS gameLibs render REQUIRES gpu TIMEOUT 1200)
endif()
