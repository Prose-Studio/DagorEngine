if(WIN32)
  list(APPEND libs System::wsock32)
endif()

dagor_add_target(NAME tools.sceneTools.daEditorX.Environment STATIC LAX
  FILES_CMAKE Environment_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${libs}
)
