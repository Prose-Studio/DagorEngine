# The tool side of the common effects (their editor classes and the effect list of prog/commonFx/fxList.jam), for the
# effect exporter and the editors. The emb variant: the build embedded in games (_TARGET_EXPORTERS_STATIC).
foreach(variant "" .emb)
  set(name commonFx.commonFxTools${variant})
  dagor_add_target(NAME ${name} STATIC LAX
    FILES_CMAKE commonFxTools_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/commonFx/commonFxGame
  )
endforeach()
target_compile_definitions(commonFx.commonFxTools.emb PRIVATE _TARGET_EXPORTERS_STATIC)
