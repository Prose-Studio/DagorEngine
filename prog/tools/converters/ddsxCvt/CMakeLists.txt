# ddsxCvt: converts DDS textures to the DDSx of a target platform through the DDSx plugins
set(includes ${DAGOR_PROG_DIR}/tools/sharedInclude)
set(sources ddsxConverter.cpp con_main.cpp)
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub tools.libTools.dtx tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_executable(ddsxCvt LAX NO_CONFIG_POSTFIX ${sources})
target_include_directories(ddsxCvt PRIVATE ${includes})
target_link_libraries(ddsxCvt PRIVATE ${deps})
dagor_install_cdk(ddsxCvt)
