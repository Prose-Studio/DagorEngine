# csq, the console Quirrel interpreter of the CDK (with the game's script bindings: http, frp, json, jwt, yup files)
if(WIN32)
  list(APPEND libs System::shell32)
endif()
# Rel builds run on mimalloc (and keep their logs: DAGOR_FORCE_LOGS of the cdk tree)
set(memory "$<IF:$<CONFIG:Rel>,engine.memory.mimalloc,engine.memory>")
set(deps engine.osApiWrappers engine.kernel ${memory} engine.ioSys engine.startup engine.baseUtil engine.coreUtil
  engine.math engine.consoleProc engine.perfMon.daProfilerStub engine.workCycle engine.lib3d engine.drv.drv3d_pc_multi
  3rdPartyLibs.eastl 3rdPartyLibs.libb64 gameLibs.quirrel.bindQuirrelEx gameLibs.quirrel.quirrel_json
  gameLibs.quirrel.http gameLibs.quirrel.frp gameLibs.quirrel.sqJwt gameLibs.quirrel.base64
  gameLibs.quirrel.asyncRuntime gameLibs.asyncHTTPClient)
if(WIN32)
  list(APPEND deps gameLibs.quirrel.win_registry)
endif()
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub engine.workCycle.stub)
endif()
list(APPEND deps gameLibs.yup_parse gameLibs.quirrel.yupfile_parse)

dagor_add_target(NAME csq EXECUTABLE
  FILES_CMAKE consoleSq_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/jsoncpp/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/squirrel
  COMPILE_DEFINITIONS PRIVATE HAS_YUP_PARSE
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE Dagor::Quirrel ${deps}
  CDK
)

# the tests it runs (in the tests tree): its script API (tests/), the engine's script tests, and the static analysis of
# the shared scripts, daNetGame's and dargbox's samples (against the native modules' stubs of their .sqconfig)
if(DAGOR_ENGINE_TESTS)
  file(GLOB tests CONFIGURE_DEPENDS tests/test_*.nut)
  foreach(test IN LISTS tests)
    cmake_path(GET test STEM name)
    dagor_add_exec_test(csq.${name} COMMAND $<TARGET_FILE:csq> ${test} WORKING_DIRECTORY tests TAGS quirrel)
  endforeach()
  foreach(test scripts/tests/rand_test.nut scripts/tests/srt_test.nut scripts/tests/string_test.nut
               scripts/sq/tests/test_memo.nut)
    cmake_path(GET test PARENT_PATH dir)
    cmake_path(GET test STEM name)
    dagor_add_exec_test(scripts.${name} COMMAND $<TARGET_FILE:csq> ${DAGOR_PROG_DIR}/${test}
      WORKING_DIRECTORY ${DAGOR_PROG_DIR}/${dir} TAGS quirrel)
  endforeach()
  file(GLOB_RECURSE scripts CONFIGURE_DEPENDS RELATIVE ${DAGOR_PROG_DIR} ${DAGOR_PROG_DIR}/scripts/sq/daRg/*.nut
    ${DAGOR_PROG_DIR}/scripts/sq/std/*.nut ${DAGOR_PROG_DIR}/scripts/sq/daeditor/*.nut
    ${DAGOR_PROG_DIR}/daNetGame/scripts/globals/*.nut ${DAGOR_PROG_DIR}/tools/dargbox/gamebase/*.nut)
  foreach(script IN LISTS scripts)
    cmake_path(GET script PARENT_PATH dir)
    dagor_add_exec_test(csq.analysis:${script} COMMAND $<TARGET_FILE:csq> --static-analysis ${DAGOR_PROG_DIR}/${script}
      WORKING_DIRECTORY ${DAGOR_PROG_DIR}/${dir} TAGS quirrel)
  endforeach()
endif()
