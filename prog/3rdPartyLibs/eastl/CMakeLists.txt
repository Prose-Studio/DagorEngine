# EASTL; its include dir is one of the base include dirs of every C++ compile (DagorCompilerFlags.cmake). The kernel
# variant is the build inside daKernel (tools/libTools/daKernel), which exports its allocator and snprintf
# (__B_KERNEL_LIB).
foreach(variant "" .kernel)
  dagor_add_target(NAME 3rdPartyLibs.eastl${variant} STATIC LAX
    FILES_CMAKE eastl_files.cmake
    INCLUDE_DIRECTORIES PRIVATE include
  )
endforeach()
target_compile_definitions(3rdPartyLibs.eastl.kernel PRIVATE __B_KERNEL_LIB)
