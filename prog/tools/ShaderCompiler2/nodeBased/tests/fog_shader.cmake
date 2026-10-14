# cmake -DNODE_BASED=<dsc2-nodeBased> -DTARGET=<dx11|dx12|spirv|metal> -DCOMPILER=<the target's dsc2-*>
#       -DDUKTAPE=<duktape> -DSHADER_INFO=<shaderInfo> -DOUT=<dir> -P fog_shader.cmake
# Compiles a node-based fog shader as daBuild's locShadersExp does: an empty graph of the web UI's fog shader editor,
# its shader code made by the editor's scripts (in duktape) and put into the fog shader template, compiled by the
# target's compiler into a dump that shaderInfo must load with the shader and its bytecode. The tool runs duktape and
# the compiler from its own dir and reads the engine's sources three dirs above it, as in the CDK and in a build tree.
foreach(var NODE_BASED TARGET COMPILER DUKTAPE SHADER_INFO OUT)
  if(NOT ${var})
    message(FATAL_ERROR "usage: cmake -DNODE_BASED=<dsc2-nodeBased> -DTARGET=<dx11|dx12|spirv|metal> "
      "-DCOMPILER=<the target's dsc2-*> -DDUKTAPE=<duktape> -DSHADER_INFO=<shaderInfo> -DOUT=<dir> -P fog_shader.cmake")
  endif()
endforeach()
cmake_path(GET NODE_BASED PARENT_PATH bin)
foreach(program IN ITEMS "${COMPILER}" "${DUKTAPE}")
  cmake_path(GET program PARENT_PATH dir)
  if(NOT dir STREQUAL bin)
    message(FATAL_ERROR "${program} is not next to ${NODE_BASED}, which runs it from its own dir")
  endif()
endforeach()
file(REMOVE_RECURSE "${OUT}")
file(WRITE "${OUT}/fog.json" [=[{
  "graphId": "[[GID:0A-1]]",
  "pluginId": "[[plugin:fog_shader_editor]]",
  "elemCount": 0,
  "edgeCount": 0,
  "hint": "[[generated_graph_hint]]",
  "view": { "posX": 0, "posY": 0, "width": 1000 },
  "selected": [],
  "elems": [],
  "edges": []
}
]=])
file(MAKE_DIRECTORY "${OUT}/subgraphs")
# native paths: the editor's scripts list the subgraphs dir with the shell's commands
file(TO_NATIVE_PATH "${OUT}/fog.json" graph)
file(TO_NATIVE_PATH "${OUT}/fog" out)
file(TO_NATIVE_PATH "${OUT}/subgraphs" subgraphs)
# in the build dir, in the engine's tree: the tool finds the shader templates above its working dir; -f: no sha1 cache
execute_process(COMMAND "${NODE_BASED}" -f -p:fog_shader_editor "-singleInputJson:${graph}" "-singleOutputBin:${out}"
    -dshlShaderName:nbs_test_fog -target:${TARGET} "-s:${subgraphs}"
  WORKING_DIRECTORY "${OUT}" RESULT_VARIABLE result OUTPUT_VARIABLE output ERROR_VARIABLE output)
if(NOT result EQUAL 0 OR NOT EXISTS "${OUT}/fog.ps50.shdump.bin")
  message(FATAL_ERROR "the node-based shader did not compile (exit code ${result}):\n${output}")
endif()

execute_process(COMMAND "${SHADER_INFO}" "${OUT}/fog.ps50.shdump.bin" "-outfile:${OUT}/shaderInfo.txt"
  RESULT_VARIABLE result OUTPUT_VARIABLE output ERROR_VARIABLE output)
if(NOT result EQUAL 0)
  message(FATAL_ERROR "shaderInfo cannot read the dump (exit code ${result}):\n${output}")
endif()
file(READ "${OUT}/shaderInfo.txt" info)
foreach(regex "Shaders bindump is intact with checksum" "--- shader\\[[0-9]+\\] - nbs_test_fog ---"
    "\\* [1-9][0-9]* pixel shaders")
  if(NOT info MATCHES "${regex}")
    message(FATAL_ERROR "shaderInfo's summary of the dump (${OUT}/shaderInfo.txt) has no match for '${regex}'")
  endif()
endforeach()
