# The AVX2 path of masked occlusion culling (x86_64 with SSE4)
set(options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set(options /arch:AVX2)
else()
  set(options -mavx2 -mfma)
endif()
set(defines)
if(DAGOR_FORCE_LINK_DEBUG_LINES)
  set(defines "$<$<CONFIG:Rel,IRel>:FORCE_LINK_DEBUG_LINES>")
endif()
dagor_add_target(NAME engine.lib3d.moc_avx STATIC
  FILES_CMAKE moc_avx_files.cmake
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
)
