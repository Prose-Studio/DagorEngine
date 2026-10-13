if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  set(deps engine.baseUtil)
endif()

dagor_add_target(NAME tools.libTools.ObjectEditor STATIC LAX
  FILES_CMAKE ObjectEditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
