if(DAGOR_BUILDING_TOOLS)
  list(APPEND defines _TARGET_PC_TOOLS_BUILD)
endif()

dagor_add_target(NAME gameLibs.webui.plugins.dagor STATIC
  FILES_CMAKE dagor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/webui ${DAGOR_PROG_DIR}/dagorInclude
  COMPILE_DEFINITIONS PRIVATE ${defines}
)
