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
  Jolt/Renderer # the debug renderer: empty where the settings do not enable it (JPH_DEBUG_RENDERER)
  Jolt/Shaders
  Jolt/Skeleton
  Jolt/TriangleSplitter
)
set(FILES Jolt/RegisterTypes.cpp)
dagor_glob_sources(FILES DIRS ${dirs} GLOB *.cpp)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set_property(SOURCE Jolt/Physics/Vehicle/MotorcycleController.cpp APPEND PROPERTY COMPILE_OPTIONS -wd4756) # overflow in constant arithmetic
  if(DAGOR_ARCH STREQUAL "arm64")
    set_property(SOURCE Jolt/Math/Vec3.cpp APPEND PROPERTY COMPILE_OPTIONS /Od) # for a correct Vec3::sUnitSphere
  endif()
endif()
