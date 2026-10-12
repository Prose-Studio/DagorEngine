# EASTL; its include dir is one of the base include dirs of every C++ compile (DagorCompilerFlags.cmake). The kernel
# variant is the build inside daKernel (tools/libTools/daKernel), which exports its allocator and snprintf
# (__B_KERNEL_LIB).
dagor_glob_sources(sources DIRS source GLOB *.cpp)
list(APPEND sources mem.cpp snprintf.cpp)
if(DAGOR_ARCH STREQUAL "e2k")
  list(APPEND sources assert_e2k.cpp)
endif()
foreach(variant "" .kernel)
  dagor_add_library(3rdPartyLibs.eastl${variant} LAX ${sources})
  target_include_directories(3rdPartyLibs.eastl${variant} PRIVATE include)
endforeach()
target_compile_definitions(3rdPartyLibs.eastl.kernel PRIVATE __B_KERNEL_LIB)
