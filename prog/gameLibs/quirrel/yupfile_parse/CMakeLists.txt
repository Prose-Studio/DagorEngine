# Quirrel module reading .yup files (through yup_parse)
if(WIN32)
  list(APPEND options /wd4548)
endif()

dagor_add_target(NAME gameLibs.quirrel.yupfile_parse STATIC
  FILES_CMAKE yupfile_parse_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/yup_parse
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel/yupfile_parse
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel engine.coreUtil
)
