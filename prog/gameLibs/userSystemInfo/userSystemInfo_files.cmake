set(FILES systemInfo.cpp dumpSysInfo.cpp userSystemInfo.cpp uuidgen.cpp redistInfo.cpp)
list(APPEND FILES systemInfo_stubext.cpp) # the fork has no systemInfo_private.cpp
