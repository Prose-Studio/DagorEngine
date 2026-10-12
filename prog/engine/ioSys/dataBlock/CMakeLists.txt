# DataBlock: the BLK text/binary format
set(sources
  blk_core.cpp
  blk_errors.cpp
  blk_parser.cpp
  blk_readBBF3.cpp
  blk_serialize.cpp
  blk_to_json.cpp
  blk_zstd.cpp
  blk_utils.cpp
  blk_writeBBF3.cpp
  obsolete_hashNameMap.cpp
)
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)
set(defines __B_KERNEL_LIB)

dagor_add_library(engine.ioSys.dataBlock ${sources})
target_include_directories(engine.ioSys.dataBlock PRIVATE ${includes})
target_compile_definitions(engine.ioSys.dataBlock PRIVATE ${defines})
set_target_properties(engine.ioSys.dataBlock PROPERTIES DAGOR_FRAME_LIMIT 262144)
