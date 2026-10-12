# RapidJSON helpers on EASTL: typed member get/set with error strings, key copies, stringify
set(includes
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
)
set(sources src/rapidJsonUtils.cpp)
list(APPEND deps 3rdPartyLibs.eastl)

dagor_add_library(1stPartyLibs.rapidJsonUtils LAX ${sources})
target_include_directories(1stPartyLibs.rapidJsonUtils PRIVATE ${includes})
target_link_libraries(1stPartyLibs.rapidJsonUtils PRIVATE ${deps})
