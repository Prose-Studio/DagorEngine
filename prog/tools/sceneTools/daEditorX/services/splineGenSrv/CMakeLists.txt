dagor_add_target(NAME tools.sceneTools.daEditorX.services.splineGenSrv STATIC LAX
  FILES_CMAKE splineGenSrv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.math.misc
)
