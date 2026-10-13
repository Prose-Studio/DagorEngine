# daBuild, the asset build of the content pipeline: daBuild (the program), daBuild-job (its worker processes) and the
# daBuild library that the editors load, all on daKernel (the assets tree, DAGOR_KERNEL_LINKAGE dynamic). The exporters
# and reference providers are plugins (exporters/, refProviders/, plugins/dabuild of the CDK).
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic" OR DAGOR_SANITIZE STREQUAL "address") # daKernel has no ASan build
  return()
endif()

set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine)
set(program_deps engine.startup engine.math engine.gameRes engine.lib3d engine.drv.drv3d_null
  engine.perfMon.daProfilerStub tools.libTools.assetMgr tools.libTools.assetMgrHlp tools.libTools.util
  tools.libTools.dtx 3rdPartyLibs.hash tools.libTools.daKernel)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND program_deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME daBuild EXECUTABLE LAX
  FILES_CMAKE assetExp_files.cmake daBuild_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE _TARGET_DABUILD_STATIC
  BUILD_DEPENDENCIES PRIVATE ${program_deps}
  CDK
)
dagor_add_target(NAME daBuild-job EXECUTABLE LAX
  FILES_CMAKE assetExp_files.cmake daBuild-job_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE _TARGET_DABUILD_STATIC
  BUILD_DEPENDENCIES PRIVATE ${program_deps} 3rdPartyLibs.arc.zlib-ng
  CDK
)
# the library of the editors (named daBuild too; its debug info is daBuild-dll.pdb, as jam named it)
dagor_add_target(NAME daBuildLib SHARED LAX OUTPUT_NAME daBuild
  FILES_CMAKE assetExp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE
    engine.startup engine.math tools.libTools.assetMgr tools.libTools.assetMgrHlp tools.libTools.util tools.libTools.dtx
    3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.hash tools.libTools.daKernel
  PROPERTIES PDB_NAME daBuild-dll
  CDK
)
