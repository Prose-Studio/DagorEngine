# TODO(jam): MaxVer ?= Max2027 ;
# TODO(jam): include $(Root)/$(Location)/maxPlugin.jam ;
dagor_add_target(NAME dagor SHARED LAX
  FILES_CMAKE maxplug_files.cmake
  INCLUDE_DIRECTORIES PRIVATE stubInclude
)
