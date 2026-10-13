# csq, the console Quirrel interpreter of the CDK (with the game's script bindings: http, frp, json, jwt, yup files)
if(WIN32)
  list(APPEND libs System::shell32)
endif()
# Rel builds run on mimalloc and keep their logs
set(memory "$<IF:$<CONFIG:Rel>,engine.memory.mimalloc,engine.memory>")
set(deps engine.osApiWrappers engine.kernel ${memory} engine.ioSys engine.startup engine.baseUtil engine.coreUtil
  engine.math engine.consoleProc engine.perfMon.daProfilerStub engine.workCycle engine.lib3d engine.drv.drv3d_stub
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
  COMPILE_DEFINITIONS PRIVATE HAS_YUP_PARSE $<$<CONFIG:Rel>:DAGOR_FORCE_LOGS>
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE Dagor::Quirrel ${deps}
  CDK
)
