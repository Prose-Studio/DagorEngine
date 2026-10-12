# The developer console: commands, variables, the console processor
set(deps 3rdPartyLibs.imgui)
set(sources
  conBaseProc.cpp
  conClassBase.cpp
  consoleProcessor.cpp
  consoleVisualDrv.cpp
  consoleState.cpp
  consoleInit.cpp
  consoleVars.cpp
  consoleUtil.cpp
  defAppConsole.cpp
  profilerConsole.cpp
)

dagor_add_library(engine.consoleProc ${sources})
target_link_libraries(engine.consoleProc PRIVATE ${deps})
