# Metronome unit tests, with mock shader variables. They run on the stub driver; in trees with a real 3d driver also on
# that one (gameLibs.metronome, requires a GPU).
set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  set(options -Wc++11-narrowing -Wswitch -Wbitfield-constant-conversion -Wmissing-field-initializers)
endif()
dagor_add_catch2_test(metronome-tests TAGS gameLibs render ARGS --gpu-driver stub main.cpp metronomeTests.cpp)
target_include_directories(metronome-tests PRIVATE ${DAGOR_PROG_DIR}/gameLibs/render/daFrameGraph
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_compile_options(metronome-tests PRIVATE ${options})
target_link_libraries(metronome-tests PRIVATE engine.memory engine.kernel engine.osApiWrappers engine.coreUtil
  engine.baseUtil engine.ioSys engine.math engine.shaders engine.lib3d engine.image engine.startup engine.workCycle
  engine.perfMon.stub engine.drv.drv3d_pc_multi engine.osApiWrappers.messageBox 3rdPartyLibs.eastl
  gameLibs.render.daFrameGraph gameLibs.render.metronome)
set_target_properties(metronome-tests PROPERTIES DAGOR_SHADER_VARS mock DAGOR_LINUX_GUI ON)
set(real_drivers ${DAGOR_D3D_DRIVERS})
list(REMOVE_ITEM real_drivers stub null)
if(real_drivers)
  dagor_add_catch2_run(metronome-tests gameLibs.metronome TAGS gameLibs render REQUIRES gpu)
endif()
