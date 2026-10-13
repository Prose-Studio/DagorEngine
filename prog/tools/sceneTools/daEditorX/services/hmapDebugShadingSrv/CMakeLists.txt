# TODO(jam): KernelLinkage ?= dynamic ;
dagor_add_target(NAME tools.sceneTools.daEditorX.services.hmapDebugShadingSrv STATIC LAX
  FILES_CMAKE hmapDebugShadingSrv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
