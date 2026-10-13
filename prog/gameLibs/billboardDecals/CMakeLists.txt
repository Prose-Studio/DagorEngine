if(IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/propsRegistry")
  list(APPEND defines HAS_PROPS_REGISTRY)
endif()

dagor_add_target(NAME gameLibs.billboardDecals STATIC
  FILES_CMAKE billboardDecals_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE engine.lib3d gameLibs.decalMatrices
)
