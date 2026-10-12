set(FILES "$<IF:$<CONFIG:Rel>,${CMAKE_CURRENT_LIST_DIR}/texDebug_stub.cpp,${CMAKE_CURRENT_LIST_DIR}/texDebug.cpp>")
