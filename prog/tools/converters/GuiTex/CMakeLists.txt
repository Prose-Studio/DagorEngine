# guiTex: builds GUI texture atlases (DDS/DDSx with coordinate BLKs) from icon folders, and unpacks them
set(includes ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/engine/sharedInclude)
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.image engine.perfMon.daProfilerStub tools.libTools.util tools.libTools.dtx 3rdPartyLibs.image.psdRead
  3rdPartyLibs.image.libpng-1.4.22)
set(sources texBuilder.cpp texUnpack.cpp winmain_con.cpp)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_executable(guiTex LAX ${sources})
target_include_directories(guiTex PRIVATE ${includes})
target_link_libraries(guiTex PRIVATE ${deps})
dagor_install_cdk(guiTex)
