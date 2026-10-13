set(FILES
  main.cpp
  console.cpp
  av_version.cpp
  av_appwnd.cpp
  canopyEditor.cpp
  av_engine.cpp
  av_assetSearchResultsWindow.cpp
  av_assetSearchResultsListControl.cpp
  av_consoleCommandProcessor.cpp
  av_mainAssetSelector.cpp
  av_tree.cpp
  av_srvEngine.cpp
  av_dagored2stub.cpp
  av_environment.cpp
  av_plugins.cpp
  av_preferencesDialog.cpp
  av_viewportWindow.cpp
  av_workCycleActRateDialog.cpp
  assetBuildCache.cpp
  av_util.cpp
  av_script_panel.cpp
  av_ecsPull.cpp
  av_das_manager.cpp
  badRefFinder.cpp
  compositeAssetCreator.cpp
  suboptimalAssetCollector.cpp
)
list(APPEND FILES dng_pulls.cpp)
set_property(SOURCE dng_pulls.cpp APPEND PROPERTY INCLUDE_DIRECTORIES ${DAGOR_PROG_DIR}/daNetGameLibs)
if(IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/ecs/phys")
  set_property(SOURCE av_das_manager.cpp APPEND PROPERTY COMPILE_DEFINITIONS HAS_PHYS)
endif()
