# dsc2-nodeBased: compiles the node-based shaders of the web UI's shader editors (the compiler flavor of
# gameLibs/webui/plugins/shaderEditors) into the dumps games load
set(deps engine.osApiWrappers engine.kernel engine.memory.default.off engine.ioSys engine.startup engine.baseUtil
  engine.math engine.perfMon.daProfilerStub gameLibs.webui.plugins.shaderEditors.comp tools.libTools.util
  3rdPartyLibs.regExp)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME dsc2-nodeBased EXECUTABLE LAX
  FILES_CMAKE nodeBased_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)

# the tests (tests/fog_shader.cmake): a node-based fog shader compiled for each target the host's compilers have, in the
# build dir: the tool looks for the shader templates above its working dir, in the engine's tree. It keeps its
# intermediate files in <engine>/build/runtime-shaders (three dirs above its own).
if(DAGOR_CDK_TESTS)
  foreach(target dx11|dsc2-hlsl11 dx12|dsc2-dx12 spirv|dsc2-spirv metal|dsc2-metal)
    string(REPLACE "|" ";" target "${target}")
    list(POP_FRONT target name compiler)
    if(NOT TARGET ${compiler})
      continue()
    endif()
    dagor_add_exec_test(dsc2-nodeBased.fog_${name} COMMAND ${CMAKE_COMMAND} -DNODE_BASED=$<TARGET_FILE:dsc2-nodeBased>
      -DTARGET=${name} -DCOMPILER=$<TARGET_FILE:${compiler}> -DDUKTAPE=$<TARGET_FILE:duktape>
      -DSHADER_INFO=$<TARGET_FILE:shaderInfo> -DOUT=${CMAKE_BINARY_DIR}/test-artifacts/dsc2-nodeBased.fog_${name}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/fog_shader.cmake TAGS cdk TIMEOUT 120)
  endforeach()
endif()
