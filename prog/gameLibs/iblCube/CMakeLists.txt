set(includes ${DAGOR_PROG_DIR}/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(SourceES render/iblCubeES.cpp.inl)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.iblCube LAX)
target_include_directories(gameLibs.iblCube PRIVATE ${includes})
dagor_target_es_sources(gameLibs.iblCube ${es_sources})
