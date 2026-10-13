# The game side of the common effects (light, sparks, modfx and compound effects of daFx; the effect list of
# the list in commonFxGame_files.cmake). The gz variant: with gravity zones (DAFX_USE_GRAVITY_ZONE).
foreach(variant "" .gz)
  set(name commonFx.commonFxGame${variant})
  dagor_add_target(NAME ${name} STATIC
    FILES_CMAKE commonFxGame_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/commonFx/commonFxGame ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    BUILD_DEPENDENCIES PRIVATE gameLibs.daFx
  )
endforeach()
target_compile_definitions(commonFx.commonFxGame.gz PRIVATE DAFX_USE_GRAVITY_ZONE)
