# DataBlock: the BLK text/binary format
dagor_add_target(NAME engine.ioSys.dataBlock STATIC
  FILES_CMAKE dataBlock_files.cmake
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
