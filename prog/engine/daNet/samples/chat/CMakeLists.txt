dagor_add_target(NAME chat EXECUTABLE LAX
  OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  FILES_CMAKE chat_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.perfMon.daProfilerStub
    engine.daNet
)
