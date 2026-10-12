# Microsoft's mimalloc, an allocator of engine/memory (engine.memory.mimalloc). Its own checks (MI_DEBUG 2) are on in
# Dev and Dbg; the nodebug variant has none (for engine.memory.mimalloc.off).
foreach(variant "" .nodebug)
  set(name 3rdPartyLibs.memAllocators.mimalloc${variant})
  dagor_add_target(NAME ${name} STATIC LAX
    FILES_CMAKE mimalloc_files.cmake
    INCLUDE_DIRECTORIES PRIVATE include mimalloc/include
    COMPILE_OPTIONS PRIVATE "$<$<C_COMPILER_ID:MSVC>:-wd4055;-wd4054>"
  )
  if(WIN32)
    target_link_libraries(${name} PUBLIC System::advapi32)
  endif()
endforeach()
target_compile_definitions(3rdPartyLibs.memAllocators.mimalloc PRIVATE "MI_DEBUG=$<IF:$<CONFIG:Rel,IRel>,0,2>")
target_compile_definitions(3rdPartyLibs.memAllocators.mimalloc.nodebug PRIVATE MI_DEBUG=0)
