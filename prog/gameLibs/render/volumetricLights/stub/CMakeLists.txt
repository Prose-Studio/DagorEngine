# Volumetric lights (VolumeLight) stubs for programs without volumetric lighting
dagor_add_target(NAME gameLibs.render.volumetricLights.stub STATIC LAX
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
