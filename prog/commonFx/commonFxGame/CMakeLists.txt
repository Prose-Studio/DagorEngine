# The game side of the common effects (light, sparks, modfx and compound effects of daFx; the effect list of
# prog/commonFx/fxList.jam). The gz variant: with gravity zones (DAFX_USE_GRAVITY_ZONE).
foreach(variant "" .gz)
  set(name commonFx.commonFxGame${variant})
  dagor_add_library(${name} paramScriptsPool.cpp dafxSparksCpu.cpp dafxModFxSystem.cpp dafxSystemDesc.cpp
    dafxEmitterDebug.cpp modfx/modfx_cpu.cpp stub/outdatedFx.cpp commonFx.cpp lightFx.cpp dafxSparks.cpp dafxModFx.cpp
    dafxCompound.cpp)
  target_include_directories(${name} PRIVATE ${DAGOR_PROG_DIR}/commonFx/commonFxGame
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
  target_link_libraries(${name} PRIVATE gameLibs.daFx)
endforeach()
target_compile_definitions(commonFx.commonFxGame.gz PRIVATE DAFX_USE_GRAVITY_ZONE)
