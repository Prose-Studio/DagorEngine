if(IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/ecs/phys" AND IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/gamePhys/ballistics")
  list(APPEND defines HAS_ECS_PHYS)
endif()

dagor_add_target(NAME gameLibs.ecs.render STATIC
  FILES_CMAKE render_files.cmake
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl gameLibs.resourcePool Dagor::Phys
)
