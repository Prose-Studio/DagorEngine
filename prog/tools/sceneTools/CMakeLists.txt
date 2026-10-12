# the dirs of prog/tools/sceneTools
add_subdirectory(csvUtil)
add_subdirectory(daEditorX)
add_subdirectory(dbldUtil)
add_subdirectory(dumpGrp)
add_subdirectory(guiShaders_commonData)
add_subdirectory(resClean)
add_subdirectory(resDiff)
add_subdirectory(resUpdate)
add_subdirectory(utils)
add_subdirectory(vromfsPacker)
if(DAGOR_KERNEL_LINKAGE STREQUAL "dynamic" AND NOT DAGOR_SANITIZE STREQUAL "address") # daBuild: on daKernel, no ASan
  add_subdirectory(assetExp)
endif()
