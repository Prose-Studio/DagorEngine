# The C runtime's allocator for the programs and libraries on daKernel (the memory manager is in daKernel)
dagor_add_target(NAME engine.memory.rtlOverride STATIC LAX
  FILES_CMAKE rtlOverride_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators
  COMPILE_DEFINITIONS PRIVATE USE_RTL_ALLOC
)
