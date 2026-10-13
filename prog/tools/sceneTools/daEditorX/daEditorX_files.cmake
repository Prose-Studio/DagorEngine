set(FILES
  dagorEd.cpp
  srvEngine.cpp
  de_apphandler.cpp
  de_appwnd.cpp
  de_appwndConCmd.cpp
  de_collision.cpp
  de_engine.cpp
  de_exportlevel.cpp
  de_ExportToDagDlg.cpp
  de_version.cpp
  dagored_main.cpp
  plugin_dlg.cpp
  de_startdlg.cpp
  de_workspace.cpp
  de_preferencesDialog.cpp
  de_ProjectSettings.cpp
  de_screenshotMetaInfoLoader.cpp
  de_cameraPresets.cpp
  de_viewportWindow.cpp
  de_environment.cpp
  de_ecsPull.cpp
  car_camera_elem.cpp
  pluginService/de_IDagorPhysImpl.cpp
  pluginService/graph_tex_gen_service.cpp
  pluginService/image_export.cpp
  pluginService/landscape_preview_service.cpp
  pluginService/texgen_dshl_assemble.cpp
  pluginService/texgen_dshl_compile.cpp
)
list(APPEND FILES dng_pulls.cpp)
set_property(SOURCE dng_pulls.cpp APPEND PROPERTY INCLUDE_DIRECTORIES ${DAGOR_PROG_DIR}/daNetGameLibs)
dagor_glob_sources(ES_FILES DIRS ecsEditor GLOB *ES.cpp.inl)
