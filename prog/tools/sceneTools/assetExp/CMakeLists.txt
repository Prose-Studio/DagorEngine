# daBuild, the asset build of the content pipeline: daBuild (the program), daBuild-job (its worker processes) and the
# daBuild library that the editors load, all on daKernel (the editor tree, DAGOR_KERNEL_LINKAGE dynamic). The exporters
# and reference providers are plugins (exporters/, refProviders/, plugins/dabuild of the CDK).
add_subdirectory(ddsxConv) # the DDSx converters of the CDK, on the static kernel too
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic" OR DAGOR_SANITIZE STREQUAL "address") # daKernel has no ASan build
  return()
endif()
add_subdirectory(exporters)
add_subdirectory(refProviders)

set(includes ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine)
set(export_sources loadPlugins.cpp texExport.cpp resExport.cpp daBuild.cpp assetExport.cpp jobPool.cpp)
set(program_deps engine.startup engine.math engine.gameRes engine.lib3d engine.drv.drv3d_null
  engine.perfMon.daProfilerStub tools.libTools.assetMgr tools.libTools.assetMgrHlp tools.libTools.util
  tools.libTools.dtx 3rdPartyLibs.hash tools.libTools.daKernel)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND program_deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_executable(daBuild LAX cmain.cpp ${export_sources})
target_include_directories(daBuild PRIVATE ${includes})
target_compile_definitions(daBuild PRIVATE _TARGET_DABUILD_STATIC)
target_link_libraries(daBuild PRIVATE ${program_deps})
dagor_install_cdk(daBuild)
dagor_add_executable(daBuild-job LAX cmain-job.cpp ${export_sources})
target_include_directories(daBuild-job PRIVATE ${includes})
target_compile_definitions(daBuild-job PRIVATE _TARGET_DABUILD_STATIC)
target_link_libraries(daBuild-job PRIVATE ${program_deps} 3rdPartyLibs.arc.zlib-ng)
dagor_install_cdk(daBuild-job)
# the library of the editors (named daBuild too; its debug info is daBuild-dll.pdb, as jam named it)
dagor_add_library(daBuildLib SHARED LAX OUTPUT_NAME daBuild ${export_sources})
target_include_directories(daBuildLib PRIVATE ${includes})
target_link_libraries(daBuildLib PRIVATE engine.startup engine.math tools.libTools.assetMgr tools.libTools.assetMgrHlp
  tools.libTools.util tools.libTools.dtx 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.hash tools.libTools.daKernel)
set_target_properties(daBuildLib PROPERTIES PDB_NAME daBuild-dll)
dagor_install_cdk(daBuildLib)
