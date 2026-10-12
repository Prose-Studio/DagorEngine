# Jolt Physics (https://github.com/jrouwe/JoltPhysics.git, rev 7b9fbc356e83e3faaef36311f2d7fd6cc9720916)
set(defines)
if(WIN32)
  list(APPEND defines _CRT_SECURE_NO_WARNINGS _CRT_SECURE_NO_DEPRECATE _SCL_SECURE_NO_WARNINGS)
endif()
set(options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND options -Wno-uninitialized) # on `index` in UnorderedMap.h
endif()
dagor_deterministic_fp(options)

dagor_add_target(NAME 3rdPartyLibs.phys.joltPhysics STATIC LAX
  FILES_CMAKE joltPhysics_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE Dagor::JoltSettings
)
