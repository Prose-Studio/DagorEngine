# das: the daScript interpreter and test runner (dastest) of the engine, with its ECS and Dagor modules; installed into
# tools/util as das[-64]-<config> for the scripts that run it
set(name das)
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  set(output_name das-64)
else()
  set(output_name das)
endif()

dagor_add_executable(${name} LAX OUTPUT_NAME ${output_name} main.cpp unitTest.cpp ../../dagorAdapter/da_dummy.cpp
  ../../dagorAdapter/da.cpp ../../modules/dasUnitTest/bytecode.cpp ../../modules/dasUnitTest/test_enum.cpp
  ../../modules/dasUnitTest/test_handles.cpp ../../modules/dasUnitTest/test_crt_math.cpp)
target_include_directories(${name} PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
target_compile_definitions(${name} PRIVATE DAS_USE_BASE_CRASH_HANDLER=1)
target_link_libraries(${name} PRIVATE engine.osApiWrappers engine.kernel engine.perfMon engine.memory.rtl
  engine.baseUtil engine.ioSys engine.startup engine.math 3rdPartyLibs.eastl 1stPartyLibs.daScript engine.daECS.core
  gameLibs.ecs.scripts.das gameLibs.dasModules.common engine.perfMon.daProfilerStub)
set_target_properties(${name} PROPERTIES DAGOR_DAS_CONSOLE ON DAGOR_NO_GPU ON)
