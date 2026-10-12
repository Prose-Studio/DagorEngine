# dlmalloc 2.8.4, the default allocator of engine/memory on Windows; the debug variant has the debug allocator checks
# (linked by engine.memory.dlmalloc.dbg and .dbg2)
foreach(variant "" .debug)
  dagor_add_library(3rdPartyLibs.memAllocators.dlmalloc${variant} LAX dlmalloc-2.8.4.c winapiMoreCore.cpp allocStep.cpp)
  target_include_directories(3rdPartyLibs.memAllocators.dlmalloc${variant} PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude)
endforeach()
target_compile_definitions(3rdPartyLibs.memAllocators.dlmalloc.debug PRIVATE MEM_DEBUGALLOC)
