# Tools utilities: strings, file paths and masks, hashing, undo system, log writers, BLK helpers, binary dumps
set(includes ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources
  str_util.cpp
  filePathName.cpp
  hash.cpp
  hashSaveCb.cpp
  undosys.cpp
  conProgressIndicator.cpp
  fileUtils.cpp
  conLogWriter.cpp
  reportLogWriter.cpp
  blockFileUtil.cpp
  fileMask.cpp
  dag_TabOps.cpp
  tab_sort.cpp
  colorUtil.cpp
  meshUtil.cpp
  binDumpUtil.cpp
  prepareBillboardMesh.cpp
  blkUtil.cpp
  svgWrite.cpp
  genericCache.cpp
  twoStepRelPath.cpp
  iesReader.cpp
)
if(WIN32)
  list(APPEND sources dagUuid.cpp str_util_shlwapi.cpp)
elseif(LINUX)
  list(APPEND sources dagUuid.cpp)
  list(APPEND libs System::uuid)
endif()
set(deps 3rdPartyLibs.hash 3rdPartyLibs.regExp)

dagor_add_library(tools.libTools.util LAX ${sources})
target_include_directories(tools.libTools.util PRIVATE ${includes})
target_link_libraries(tools.libTools.util PRIVATE ${deps})
target_link_libraries(tools.libTools.util PUBLIC ${libs})
