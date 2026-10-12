# daScript modules of the games (prog/gameLibs/das/common.jam): pull.cpp references them; with DAGOR_DAS_AOT their
# scripts are compiled into the library
set(defines)
if(DAGOR_DAS_AOT)
  set(defines BUILD_AOT_LIB) # pull.cpp then names the AOT pull
endif()
dagor_add_target(NAME gameLibs.das.math STATIC LAX
  FILES_CMAKE math_files.cmake
  COMPILE_DEFINITIONS PRIVATE ${defines}
  DAS_PULL math_aot_DAS_pull_AOT
)
