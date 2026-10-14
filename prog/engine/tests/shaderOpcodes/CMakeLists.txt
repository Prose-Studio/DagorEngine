# The shader opcode format (shaders/shOpcodeFormat.h): its encoders and decoders round-trip every field
dagor_add_catch2_test(NAME shaderOpcodes-tests LAX
  TAGS engine
  FILES_CMAKE shaderOpcodes_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
