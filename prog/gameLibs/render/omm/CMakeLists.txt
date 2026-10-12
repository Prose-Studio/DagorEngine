# Opacity micromaps for ray tracing baked with NVIDIA's OMM SDK (Windows and Linux x86_64; a stub elsewhere)
if(WIN32)
  list(APPEND options /Zc:__cplusplus)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # a function-style macro: CMake's COMPILE_DEFINITIONS cannot hold those
  list(APPEND options "-DOMM_DEPRECATED_MSG(X)=" -Wno-ignored-attributes)
  if(LINUX AND DAGOR_ARCH STREQUAL "x86_64")
    list(APPEND options -Wno-switch)
  endif()
endif()

dagor_add_target(NAME gameLibs.render.omm STATIC LAX
  FILES_CMAKE omm_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/omm_sdk/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/omm_sdk/src ${DAGOR_PROG_DIR}/3rdPartyLibs/omm_sdk/shaders
    ${DAGOR_PROG_DIR}/3rdPartyLibs/stb ${DAGOR_PROG_DIR}/3rdPartyLibs/hash ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/lz4
  COMPILE_DEFINITIONS PRIVATE
    GLM_ENABLE_EXPERIMENTAL OMM_VK_S_SHIFT=0 OMM_VK_T_SHIFT=128 OMM_VK_B_SHIFT=256 OMM_VK_U_SHIFT=384
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE engine.lib3d engine.shaders 3rdPartyLibs.eastl 3rdPartyLibs.hash 3rdPartyLibs.arc.lz4
)
