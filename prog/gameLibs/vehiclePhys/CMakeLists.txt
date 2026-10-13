# Vehicle physics (ray cars) on each physics engine, gameLibs.vehiclePhys.jolt and .bullet (
# -BULLET); gameLibs.vehiclePhys is the tree's (DAGOR_PHYS)
foreach(phys Jolt Bullet)
  string(TOLOWER "${phys}" name)
  string(TOUPPER "${phys}" prefix)
  dagor_add_target(NAME gameLibs.vehiclePhys.${name} STATIC LAX
    FILES_CMAKE vehiclePhys_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
    COMPILE_DEFINITIONS PRIVATE RayCar=${prefix}RayCar LegacyRenderableRayCar=${prefix}LegacyRenderableRayCar
    BUILD_DEPENDENCIES PRIVATE gameLibs.vehiclePhys.carDynamics Dagor::Phys${phys}
  )
endforeach()
string(TOLOWER "${DAGOR_PHYS}" name)
add_library(gameLibs.vehiclePhys ALIAS gameLibs.vehiclePhys.${name})
