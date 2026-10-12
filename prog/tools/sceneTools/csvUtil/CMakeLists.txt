# csvUtil2: processes localization CSV files by BLK tasks; inserts word breaks into Japanese and Chinese text
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.coreUtil engine.perfMon.daProfilerStub 3rdPartyLibs.regExp)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME csvUtil2 EXECUTABLE LAX
  FILES_CMAKE csvUtil_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
