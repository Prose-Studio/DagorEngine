# The shader system: bindumps, shader variables and blocks, materials, shader meshes, scenes, render states.
#
# The shader variables come from engine.shaders.vars (the bindump's) or, in programs that set the DAGOR_SHADER_VARS
# target property, from a mock (mock: tests of render code) or a stub (stub); see dagor_add_link_select().
set(defines)
if(DAGOR_BUILDING_TOOLS)
  list(APPEND defines SHADERS_ALLOW_2_BINDUMP)
endif()
# the C++ stcode (shaders_files.cmake adds its sources)
set(stcode ${DAGOR_CPP_STCODE})
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64" AND NOT DAGOR_SSE EQUAL 4)
  set(stcode disable)
endif()
if(stcode MATCHES "^(enable|both|validate)$")
  list(APPEND defines CPP_STCODE)
  if(stcode STREQUAL "validate")
    list(APPEND defines VALIDATE_CPP_STCODE)
  endif()
  if(DAGOR_CPP_STCODE_BRANCHED)
    list(APPEND defines CPP_STCODE_DYNAMIC_BRANCHING)
  endif()
endif()
if(DAGOR_SHADERS_CAM_STUB)
  list(APPEND defines CAM_STUB)
endif()
if(DAGOR_PROFILE_STCODE)
  list(APPEND defines PROFILE_STCODE)
endif()

foreach(vars vars varsMock varsStub)
  dagor_add_target(NAME engine.shaders.${vars} STATIC LAX
    FILES_CMAKE ${vars}_files.cmake
    COMPILE_DEFINITIONS PRIVATE ${defines}
  )
endforeach()
dagor_add_link_select(engine.shaders.variables PROPERTY DAGOR_SHADER_VARS DEFAULT engine.shaders.vars
  mock engine.shaders.varsMock stub engine.shaders.varsStub)

dagor_add_target(NAME engine.shaders STATIC LAX
  FILES_CMAKE shaders_files.cmake
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE
    engine.shaders.variables 3rdPartyLibs.eastl 3rdPartyLibs.meshoptimizer 3rdPartyLibs.hash.BLAKE3
)
