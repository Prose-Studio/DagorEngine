# the profiler outside Rel, the stub in Rel
set(FILES levelProfiler.cpp src/levelProfilerExporter.cpp src/levelProfilerUI.cpp src/dataModules/textureModule.cpp
  src/dataModules/riModule.cpp src/uiComponents/levelProfilerTableBase.cpp src/uiComponents/levelProfilerWidgets.cpp
  src/uiComponents/levelProfilerFilter.cpp src/uiModules/levelProfilerTextureTable.cpp
  src/uiModules/levelProfilerRiTable.cpp)
list(TRANSFORM FILES REPLACE "^(.+)$" "$<$<NOT:$<CONFIG:Rel>>:${CMAKE_CURRENT_LIST_DIR}/\\1>")
list(APPEND FILES "$<$<CONFIG:Rel>:${CMAKE_CURRENT_LIST_DIR}/levelProfilerStub.cpp>")
