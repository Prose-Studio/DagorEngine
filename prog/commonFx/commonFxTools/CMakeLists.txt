# The tool side of the common effects (their editor classes and the effect list of prog/commonFx/fxList.jam), for the
# effect exporter and the editors. The emb variant: the build embedded in games (_TARGET_EXPORTERS_STATIC).
foreach(variant "" .emb)
  set(name commonFx.commonFxTools${variant})
  dagor_add_library(${name} LAX effectClassTools.cpp commonFxTools.cpp outdatedFxTools.cpp dafxEmitter_tools.cpp
    lightfxShadow_tools.cpp lightFx_tools.cpp dafxSparks_tools.cpp dafxModFx_tools.cpp dafxCompound_tools.cpp)
  target_include_directories(${name} PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
    ${DAGOR_PROG_DIR}/commonFx/commonFxGame)
endforeach()
target_compile_definitions(commonFx.commonFxTools.emb PRIVATE _TARGET_EXPORTERS_STATIC)
