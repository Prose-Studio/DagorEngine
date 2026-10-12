# daECS bindings of daScript: entity systems, events and queries in scripts
if(DAGOR_DAS_LLVM_AOT)
  list(APPEND defines DAS_LLVM_AOT)
endif()
if(WIN32)
  list(APPEND options /bigobj)
endif()
if(IS_DIRECTORY "${DAGOR_PROG_DIR}/engine/daECS/net")
  list(APPEND defines HAS_DANET)
endif()

dagor_add_target(NAME gameLibs.ecs.scripts.das STATIC
  FILES_CMAKE das_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/engine/dagorInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript engine.workCycle
)
