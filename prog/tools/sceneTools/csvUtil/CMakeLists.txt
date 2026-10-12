# csvUtil2: processes localization CSV files by BLK tasks; inserts word breaks into Japanese and Chinese text
set(sources csvUtil.cpp cmain.cpp japan.cpp chinese.cpp)
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.coreUtil engine.perfMon.daProfilerStub 3rdPartyLibs.regExp)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_executable(csvUtil2 LAX ${sources})
target_link_libraries(csvUtil2 PRIVATE ${deps})
dagor_install_cdk(csvUtil2)
