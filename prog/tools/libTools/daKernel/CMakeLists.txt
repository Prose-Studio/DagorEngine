# daKernel, the shared engine kernel of the tools of the editor tree (DAGOR_KERNEL_LINKAGE dynamic): the OS wrappers,
# kernel, memory manager (on the C runtime's allocator), I/O, base utilities, profiler and EASTL, exported to the
# tools and their plugins, which import them instead of linking their own copies
set(deps engine.osApiWrappers engine.kernel engine.memory.rtl engine.ioSys engine.baseUtil engine.perfMon
  engine.perfMon.daProfiler 3rdPartyLibs.eastl.kernel)
set(options)
set(libs)
set(link_options)
if(WIN32)
  list(APPEND deps engine.osApiWrappers.messageBox)
  set(libs System::dbghelp System::user32)
elseif(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub engine.workCycle.stub)
  set(libs System::dl System::pthread System::rt System::m System::stdc++)
  set(link_options -Wl,--no-undefined)
  # only what the kernel exports (KRNLIMP) is visible outside the library
  set(options -fvisibility=hidden)
endif()

dagor_add_library(tools.libTools.daKernel SHARED OUTPUT_NAME daKernel daKernel.cpp namedPtr.cpp gpFuncTable.cpp)
target_include_directories(tools.libTools.daKernel PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
  ${DAGOR_PROG_DIR}/engine/sharedInclude)
target_compile_definitions(tools.libTools.daKernel PRIVATE __B_KERNEL_LIB)
target_compile_options(tools.libTools.daKernel PRIVATE ${options})
target_link_libraries(tools.libTools.daKernel PRIVATE ${deps})
target_link_libraries(tools.libTools.daKernel PUBLIC ${libs})
target_link_options(tools.libTools.daKernel PRIVATE ${link_options})
dagor_install_cdk(tools.libTools.daKernel)
