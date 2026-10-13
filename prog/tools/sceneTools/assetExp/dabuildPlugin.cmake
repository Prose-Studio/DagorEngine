# dabuild_plugin(NAME <name> <dagor_add_target arguments>): a daBuild plugin (an exporter or reference provider) in
# plugins/dabuild of the CDK, on daKernel with the asset manager helpers (jam's dabuild_plugin_common.jam); included by
# the plugins' directories
include_guard(GLOBAL)
function(dabuild_plugin)
  dagor_add_target(${ARGN} SHARED LAX
    OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/plugins/dabuild
    CDK_SUBDIR plugins/dabuild
  )
  cmake_parse_arguments(PARSE_ARGV 0 arg "" "NAME" "")
  target_link_libraries(${arg_NAME} PRIVATE tools.libTools.assetMgrHlp tools.libTools.util tools.libTools.daKernel)
endfunction()
