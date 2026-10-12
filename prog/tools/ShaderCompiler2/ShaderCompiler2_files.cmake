# the front end of every dsc2 compiler
set(FILES
  shaderVariantSrc.cpp winmain_con.cpp main.cpp globVarSem.cpp shSemCode.cpp assemblyShader.cpp variablesMerger.cpp
  gatherVar.cpp semUtils.cpp shExpr.cpp shExprParser.cpp shlexterm.cpp shLocVar.cpp shMacro.cpp shsem.cpp sh_stat.cpp
  shCompiler.cpp debugSpitfile.cpp globalConfig.cpp hwSemantic.cpp hwAssembly.cpp shaderSemantic.cpp
  variantSemantic.cpp variantAssembly.cpp preshaderCompilation.cpp gatherVariantLocalVars.cpp
  shCode.cpp shTargetStorage.cpp shAssumes.cpp shaderBytecodeCache.cpp cppStcode.cpp cppStcodeAssembly.cpp
  cppStcodePasses.cpp hlslRegisters.cpp globvar.cpp intervals.cpp samplers.cpp boolVar.cpp boolExpr.cpp
  shaderVariant.cpp shaderSave.cpp shLog.cpp shUtils.cpp shFunc.cpp shCompilationInfo.cpp loadShaders.cpp
  binDumpUtils.cpp makeShBinDump.cpp transcodeShader.cpp namedConst.cpp renderPassObject.cpp framebufferLayout.cpp
  refinedBlockLayout.cpp refinedBlockRegisterAllocator.cpp codeBlocks.cpp condParser.cpp deSerializationContext.cpp
  linkShaders.cpp parser/bparser.cpp gitRunner.cpp processes.cpp
)
if(WIN32)
  list(APPEND FILES processes_win.cpp)
else()
  list(APPEND FILES processes_unix.cpp)
endif()
# the predefined declarations of each target, embedded into hwAssembly.cpp
file(GLOB STRINGIFY_FILES RELATIVE "${CMAKE_CURRENT_LIST_DIR}" CONFIGURE_DEPENDS
  "${CMAKE_CURRENT_LIST_DIR}/predefines_*.hlsl")
