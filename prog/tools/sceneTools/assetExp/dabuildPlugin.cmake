# dabuild_plugin(<name> <source>...): a daBuild plugin (an exporter or reference provider) in plugins/dabuild of the
# CDK, on daKernel with the asset manager helpers (jam's dabuild_plugin_common.jam); included by the plugins'
# directories
include_guard(GLOBAL)
function(dabuild_plugin name)
  dagor_add_library(${name} SHARED LAX OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/plugins/dabuild ${ARGN})
  target_link_libraries(${name} PRIVATE tools.libTools.assetMgrHlp tools.libTools.util tools.libTools.daKernel)
  dagor_install_cdk(${name} SUBDIR plugins/dabuild)
endfunction()
