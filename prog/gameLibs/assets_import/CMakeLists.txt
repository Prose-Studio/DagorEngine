# The in-game asset manager (DAGOR_GAME_ASSET_MANAGER, outside Rel): daBuild built into the client builds the assets it
# loads and rebuilds them when they change; its daScript reloads them. Without it, and in Rel, the stub.
list(APPEND deps Dagor::Phys)
if(DAGOR_GAME_ASSET_MANAGER)
  foreach(lib tools.libTools.assetMgr tools.libTools.assetMgrHlp.emb tools.libTools.dtx tools.sceneTools.assetExp)
    list(APPEND deps "$<$<NOT:$<CONFIG:Rel>>:${lib}>")
  endforeach()
endif()
dagor_add_dng_module(NAME gameLibs.assets_import DAS
  FILES_CMAKE assets_import_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/tools/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
# the asset manager's DDSx converter plugin, the CDK's, in plugins/ next to the game
if(DAGOR_GAME_ASSET_MANAGER)
  dagor_host_tool(pcDdsxConv ddsx_plugin FILE plugins/ddsx/pcDdsxConv${CMAKE_SHARED_LIBRARY_SUFFIX})
  if(TARGET ${ddsx_plugin_DEPENDS}) # the CDK built on demand (not a prebuilt one, DAGOR_HOST_TOOLS_DIR)
    add_dependencies(gameLibs.assets_import ${ddsx_plugin_DEPENDS})
  endif()
  set_property(TARGET gameLibs.assets_import APPEND PROPERTY INTERFACE_DAGOR_RUNTIME_FILES
    "$<$<NOT:$<CONFIG:Rel>>:plugins|${ddsx_plugin}>")
endif()
