set(FILES exposureCompute.cpp adaptationSettingsEcs.cpp
  "$<$<CONFIG:Dev,Dbg>:${CMAKE_CURRENT_LIST_DIR}/adaptationDebug.cpp>")
