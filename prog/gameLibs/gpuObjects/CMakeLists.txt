# GPU objects: the GPU placement of small objects on surfaces (rendinst decorations), with the volume placer ES
dagor_add_library(gameLibs.gpuObjects gpuObjects.cpp)
target_include_directories(gameLibs.gpuObjects PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${CMAKE_CURRENT_SOURCE_DIR})
dagor_target_es_sources(gameLibs.gpuObjects volumePlacerES.cpp.inl)
