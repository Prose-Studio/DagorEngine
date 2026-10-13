# TODO(jam): KernelLinkage ?= dynamic ;
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  # TODO(jam): include $(Root)/prog/tools/sceneTools/daEditorX/HeightmapLand/jamfile-aces ;
  # TODO(jam): return ;
endif()
# TODO(jam): Dependencies = $(Root)/$(Location)/jamfile-classic $(Root)/$(Location)/jamfile-aces ;

dagor_add_target(NAME Hmap_plugin_dll STATIC LAX)
