# System information (OS, CPU, GPU and memory) for logs and crash reports; a stub where a platform has none
if(WIN32)
  list(APPEND includes ${DAGOR_ENGINE_ROOT}/3rdPartyLibs/eastl/include)
  set(sources win/systemId.cpp)
  list(APPEND libs System::advapi32)
else()
  set(sources stub/sysinfo.cpp)
endif()

dagor_add_library(1stPartyLibs.sysinfo ${sources})
target_include_directories(1stPartyLibs.sysinfo PRIVATE ${includes})
target_link_libraries(1stPartyLibs.sysinfo PUBLIC ${libs})
