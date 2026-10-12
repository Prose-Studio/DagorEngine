dagor_add_target(NAME gameLibs.render.levelProfiler STATIC
  FILES_CMAKE levelProfiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/rendInst
    ${DAGOR_PROG_DIR}/gameLibs/render/levelProfiler/include
    ${DAGOR_PROG_DIR}/gameLibs/render/levelProfiler/include/dataModules
    ${DAGOR_PROG_DIR}/gameLibs/render/levelProfiler/include/uiComponents
    ${DAGOR_PROG_DIR}/gameLibs/render/levelProfiler/include/uiModules
)
