set(FILES dynRender.cpp renderHelperSrv.cpp thermalVision.cpp)
set(SourceES tonemapUpdES.cpp.inl)
# TODO(jam): if $(ToolsHaveVR) = yes { CPPopt += -DTOOLS_HAVE_VR ; Target = $(Target:S=~vr.lib) ; }
set(ES_FILES ${SourceES})
# TODO(jam): include $(Root)/prog/gameLibs/render/ambientOcclusion/_lib.jam ;
set(SourceES )
