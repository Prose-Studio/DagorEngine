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
if(IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/ecs/phys")
  set_property(SOURCE av_das_manager.cpp APPEND PROPERTY COMPILE_OPTIONS -DHAS_PHYS)
endif()
# TODO(jam): include $(Root)/$(Location)/_libs.jam ;
# TODO(jam): gamePulls_action = make_module_pull_cpp ;
list(APPEND FILES gamePulls.jamvar)
# TODO(jam): gameVersion = unsigned get_exe_version32(){return 0;} char const *get_exe_version_str(){return
#   \"0.0.0.0\";} int get_build_number(){ return -1;} ;
list(APPEND FILES dng_pulls.cpp)
set_property(SOURCE dng_pulls.cpp APPEND PROPERTY COMPILE_OPTIONS -I$(Root)/prog/daNetGameLibs)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  # TODO(jam): include $(Root)/prog/tools/sceneTools/assetExp/dabuild_static.jam ;
  # TODO(jam): Dependencies += $(Root)/prog/tools/sceneTools/assetExp/jamfile-lib.jam ;
  # TODO(jam): ImportProgLibs =  ;
  set_property(SOURCE main.cpp APPEND PROPERTY COMPILE_OPTIONS -I $(Root)/prog/tools/libTools/daKernel)
endif()
