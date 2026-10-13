# extractSkins and extractDecals: the skins and decals of the assets, next to their sources as jam built them
foreach(tool extractSkins extractDecals)
  dagor_add_target(NAME ${tool} EXECUTABLE LAX OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    FILES_CMAKE ${tool}_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
    BUILD_DEPENDENCIES PRIVATE
      engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.ioSys engine.startup engine.math
      engine.perfMon.daProfilerStub tools.libTools.assetMgr tools.libTools.util 3rdPartyLibs.hash
  )
endforeach()
