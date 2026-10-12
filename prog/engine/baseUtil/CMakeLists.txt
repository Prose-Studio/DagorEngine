# Base utilities: strings, hashing, fast name maps, time, threads helpers
dagor_add_target(NAME engine.baseUtil STATIC
  FILES_CMAKE baseUtil_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
