list(APPEND deps 3rdPartyLibs.eastl gameLibs.resourcePool)
if(IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/ecs/phys" AND IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/gamePhys/ballistics")
  list(APPEND defines HAS_ECS_PHYS)
endif()
list(APPEND deps Dagor::Phys)

dagor_add_target(NAME gameLibs.ecs.render STATIC
  FILES_CMAKE render_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
