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

dagor_add_target(NAME tools.libTools.daKernel SHARED OUTPUT_NAME daKernel
  FILES_CMAKE daKernel_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB
  COMPILE_OPTIONS PRIVATE ${options}
  LINK_OPTIONS PRIVATE ${link_options}
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
  CDK
)
