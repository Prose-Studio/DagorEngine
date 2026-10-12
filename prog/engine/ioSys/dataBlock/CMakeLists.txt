# DataBlock: the BLK text/binary format
dagor_add_target(NAME engine.ioSys.dataBlock STATIC
  FILES_CMAKE dataBlock_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
