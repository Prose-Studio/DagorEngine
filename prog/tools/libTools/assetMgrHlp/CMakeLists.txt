# The asset manager's build helpers: the build caches of daBuild, its plugins' globals, texture conversion and asset
# references. The emb variant: the build embedded in games (gameLibs/assets_import, _TARGET_EXPORTERS_STATIC).
foreach(variant "" .emb)
  set(name tools.libTools.assetMgrHlp${variant})
  dagor_add_library(${name} LAX assetBuildCache.cpp assetExpCache.cpp assetRefsCache.cpp daBuildPluginGlobals.cpp
    texConvCache.cpp texAssetBuilderTextureFactory.cpp reloadTexAsset.cpp refProviders.cpp assetLocalProps.cpp
    assetMgrHlp.cpp assetTags.cpp assetUtils.cpp)
  target_include_directories(${name} PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude
    ${DAGOR_PROG_DIR}/engine/sharedInclude)
  target_link_libraries(${name} PRIVATE 3rdPartyLibs.hash)
endforeach()
target_compile_definitions(tools.libTools.assetMgrHlp.emb PRIVATE _TARGET_EXPORTERS_STATIC)
