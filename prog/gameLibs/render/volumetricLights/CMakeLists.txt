add_subdirectory(stub)

dagor_add_target(NAME gameLibs.render.volumetricLights STATIC LAX
  FILES_CMAKE volumetricLights_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
