# Quirrel module reading .yup files (through yup_parse)
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/yup_parse
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel/yupfile_parse
)
set(sources yupfile_parse.cpp)
set(deps engine.coreUtil)
if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_library(gameLibs.quirrel.yupfile_parse ${sources})
target_include_directories(gameLibs.quirrel.yupfile_parse PRIVATE ${includes})
target_compile_options(gameLibs.quirrel.yupfile_parse PRIVATE ${options})
target_link_libraries(gameLibs.quirrel.yupfile_parse PRIVATE Dagor::Quirrel ${deps})
