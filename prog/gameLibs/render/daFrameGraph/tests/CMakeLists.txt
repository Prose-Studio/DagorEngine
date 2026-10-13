# daFrameGraph unit tests, with mock shader variables. They run on the stub driver (cases that need a GPU skip
# themselves); in trees with a real 3d driver also on that one (gameLibs.daFrameGraph, requires a GPU).
set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  set(options -Wc++11-narrowing -Wswitch -Wbitfield-constant-conversion -Wmissing-field-initializers)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set(options /wd4458) # locals that hide members
endif()
dagor_add_catch2_test(NAME daFrameGraph-tests
  TIMEOUT 1200
  TAGS gameLibs render
  ARGS --gpu-driver stub
  FILES_CMAKE tests_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ..
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.coreUtil engine.baseUtil engine.ioSys engine.math
    engine.shaders engine.lib3d engine.image engine.startup engine.workCycle engine.perfMon.stub
    engine.drv.drv3d_pc_multi engine.osApiWrappers.messageBox 3rdPartyLibs.eastl gameLibs.render.daFrameGraph
  PROPERTIES DAGOR_SHADER_VARS mock DAGOR_LINUX_GUI ON
)
set(real_drivers ${DAGOR_D3D_DRIVERS})
list(REMOVE_ITEM real_drivers stub null)
if(real_drivers)
  dagor_add_catch2_run(daFrameGraph-tests gameLibs.daFrameGraph TAGS gameLibs render REQUIRES gpu TIMEOUT 1200)
endif()
