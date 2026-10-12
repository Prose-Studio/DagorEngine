# The C runtime's allocator for the programs and libraries on daKernel (the memory manager is in daKernel)
dagor_add_library(engine.memory.rtlOverride LAX stubRtl.cpp)
target_include_directories(engine.memory.rtlOverride PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators)
target_compile_definitions(engine.memory.rtlOverride PRIVATE USE_RTL_ALLOC)
