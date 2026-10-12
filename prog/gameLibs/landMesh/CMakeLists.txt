# The land mesh (heightmap terrain with clipmap texturing, micro details and the weight atlas); its clipmap debug UI
# (ImGui) in Dev and Dbg
set(deps gameLibs.landMesh.rendinstIntegration gameLibs.heightmap gameLibs.physMap 3rdPartyLibs.eastl engine.daBVH
  3rdPartyLibs.convert.fastDXT)
set(debug "$<CONFIG:Dev,Dbg>")
list(APPEND deps "$<${debug}:3rdPartyLibs.imgui>" "$<${debug}:engine.imgui>")
set(options)
# no fused multiply-adds and no unsafe math: the land heights must match on every platform
dagor_deterministic_fp(options)

dagor_add_target(NAME gameLibs.landMesh STATIC LAX
  FILES_CMAKE landMesh_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/gamePhys/collision
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine/lib3d ${DAGOR_PROG_DIR}/3rdPartyLibs
  COMPILE_DEFINITIONS PRIVATE VECMATH_NO_FMA
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
