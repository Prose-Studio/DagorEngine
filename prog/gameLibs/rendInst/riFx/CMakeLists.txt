add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})

dagor_add_library(gameLibs.rendInst.riFx LAX ${sources})
target_include_directories(gameLibs.rendInst.riFx PRIVATE ${includes})
