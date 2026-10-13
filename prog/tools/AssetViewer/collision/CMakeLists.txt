dagor_add_target(NAME tools.AssetViewer.collision STATIC LAX
  FILES_CMAKE collision_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/math/vhacd
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.math.vhacd tools.libTools.collision
)
