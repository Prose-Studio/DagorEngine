# The game side of the common effects (light, sparks, modfx and compound effects of daFx; the effect list of
# the list in commonFxGame_files.cmake), with gravity zones (DAFX_USE_GRAVITY_ZONE) in the programs that set
# DAGOR_DAFX_GRAVITY_ZONE (AssetViewer, dbldUtil); see dagor_add_link_choice().
foreach(variant .plain .gz)
  set(name commonFx.commonFxGame${variant})
  dagor_add_target(NAME ${name} STATIC
    FILES_CMAKE commonFxGame_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/commonFx/commonFxGame ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    BUILD_DEPENDENCIES PRIVATE gameLibs.daFx
  )
endforeach()
target_compile_definitions(commonFx.commonFxGame.gz PRIVATE DAFX_USE_GRAVITY_ZONE)
dagor_add_link_choice(commonFx.commonFxGame PROPERTY DAGOR_DAFX_GRAVITY_ZONE
  ON commonFx.commonFxGame.gz OFF commonFx.commonFxGame.plain)
