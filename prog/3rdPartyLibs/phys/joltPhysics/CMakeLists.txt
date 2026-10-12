# Jolt Physics (https://github.com/jrouwe/JoltPhysics.git, rev 7b9fbc356e83e3faaef36311f2d7fd6cc9720916)
if(NOT CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows|iOS|tvOS)$")
  message(FATAL_ERROR "Jolt: ${DAGOR_PLATFORM} is not supported")
endif()
set(dirs
  Jolt/AABBTree
  Jolt/Compute
  Jolt/Compute/CPU
  Jolt/Compute/DX12
  Jolt/Compute/VK
  Jolt/Core
  Jolt/Geometry
  Jolt/Math
  Jolt/ObjectStream
  Jolt/Physics
  Jolt/Physics/Body
  Jolt/Physics/Character
  Jolt/Physics/Collision
  Jolt/Physics/Collision/BroadPhase
  Jolt/Physics/Collision/Shape
  Jolt/Physics/Constraints
  Jolt/Physics/Hair
  Jolt/Physics/Ragdoll
  Jolt/Physics/SoftBody
  Jolt/Physics/Vehicle
  Jolt/Shaders
  Jolt/Skeleton
  Jolt/TriangleSplitter
)
set(sources Jolt/RegisterTypes.cpp)
dagor_glob_sources(sources DIRS ${dirs} GLOB *.cpp)
# the debug renderer where the settings enable it
dagor_glob_sources(renderer DIRS Jolt/Renderer GLOB *.cpp)
foreach(file IN LISTS renderer)
  list(APPEND sources "$<${DAGOR_JOLT_DEBUG}:${file}>")
endforeach()

set(defines)
if(WIN32)
  list(APPEND defines _CRT_SECURE_NO_WARNINGS _CRT_SECURE_NO_DEPRECATE _SCL_SECURE_NO_WARNINGS)
endif()
set(options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND options -Wno-uninitialized) # on `index` in UnorderedMap.h
endif()
dagor_deterministic_fp(options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set_property(SOURCE Jolt/Physics/Vehicle/MotorcycleController.cpp APPEND PROPERTY COMPILE_OPTIONS -wd4756) # overflow in constant arithmetic
  if(DAGOR_ARCH STREQUAL "arm64")
    set_property(SOURCE Jolt/Math/Vec3.cpp APPEND PROPERTY COMPILE_OPTIONS /Od) # for a correct Vec3::sUnitSphere
  endif()
endif()

dagor_add_library(3rdPartyLibs.phys.joltPhysics LAX ${sources})
target_include_directories(3rdPartyLibs.phys.joltPhysics PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_definitions(3rdPartyLibs.phys.joltPhysics PRIVATE ${defines})
target_compile_options(3rdPartyLibs.phys.joltPhysics PRIVATE ${options})
target_link_libraries(3rdPartyLibs.phys.joltPhysics PRIVATE Dagor::JoltSettings)
