# ddsx2dds: converts DDSx textures back to DDS (PC formats) and dumps their headers
set(includes ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/engine/sharedInclude)
set(sources ddsx2dds.cpp)
set(deps engine.osApiWrappers engine.osApiWrappers.messageBox.stub engine.kernel engine.memory engine.ioSys
  engine.startup engine.baseUtil engine.math engine.perfMon.daProfilerStub)

dagor_add_executable(ddsx2dds LAX NO_CONFIG_POSTFIX ${sources})
target_include_directories(ddsx2dds PRIVATE ${includes})
target_link_libraries(ddsx2dds PRIVATE ${deps})
dagor_install_cdk(ddsx2dds)
