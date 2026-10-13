# The asset manager's build helpers: the build caches of daBuild, its plugins' globals, texture conversion and asset
# references. The emb variant: the build embedded in games (gameLibs/assets_import, _TARGET_EXPORTERS_STATIC).
foreach(variant "" .emb)
  set(name tools.libTools.assetMgrHlp${variant})
  dagor_add_target(NAME ${name} STATIC LAX
    FILES_CMAKE assetMgrHlp_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
    BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.hash
  )
endforeach()
target_compile_definitions(tools.libTools.assetMgrHlp.emb PRIVATE _TARGET_EXPORTERS_STATIC)
