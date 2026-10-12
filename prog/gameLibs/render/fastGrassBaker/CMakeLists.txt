set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
# the baker on Windows outside Rel and IRel, the stub elsewhere
set(baker 0)
if(WIN32)
  set(baker "$<NOT:$<CONFIG:Rel,IRel>>")
  set(deps "$<${baker}:3rdPartyLibs.image.tiff-4.4.0>" "$<${baker}:3rdPartyLibs.convert.ispc_texcomp>")
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/convert/ispc_texcomp ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/gameLibs/rendInst)
endif()

dagor_add_target(NAME gameLibs.render.fastGrassBaker STATIC
  FILES_CMAKE fastGrassBaker_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
