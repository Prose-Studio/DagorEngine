# cmake -DCOMPILER=<dsc2-*> -DSHADER_INFO=<shaderInfo> -DBLK=<shaders_guiMinimal.blk> -DOUT=<dir> [-DSTUB=ON]
#       -P gui_shaders.cmake
# Compiles the tools' GUI shaders (tools/sceneTools/guiShaders_commonData) twice from scratch, each run in dirs of its
# own: the dumps must be byte-identical (without their blk hash, which covers the intermediate dir) and shaderInfo must
# load the dump, its checksum verified, with the set's shaders, the variable their variants depend on, their bytecode.
# STUB: the stub compiler, which makes no bytecode, only the mini dump (the shaders' descriptions daBuild exports with).
# The dump stays in OUT/gui.shdump.bin, the input of shaderInfo's tests.
foreach(var COMPILER SHADER_INFO BLK OUT)
  if(NOT ${var})
    message(FATAL_ERROR "usage: cmake -DCOMPILER=<dsc2-*> -DSHADER_INFO=<shaderInfo> -DBLK=<shaders_guiMinimal.blk> "
      "-DOUT=<dir> [-DSTUB=ON] -P gui_shaders.cmake")
  endif()
endforeach()
file(REMOVE_RECURSE "${OUT}")
cmake_path(GET BLK PARENT_PATH blk_dir)
foreach(run 1 2)
  set(dir "${OUT}/run${run}")
  # the set's blk (an absolute include path goes after :/) with the dump here
  if(STUB)
    set(dump "outDumpName:t=\"*\"\noutMiniDumpName:t=\"${dir}/gui\"")
  else()
    set(dump "outDumpName:t=\"${dir}/gui\"")
  endif()
  file(WRITE "${dir}/shaders.blk" "include \":/${BLK}\"\n${dump}\n")
  # as the build compiles them (dagor_add_shaders), in the blk's dir (the base of its relative paths), the intermediate
  # files and the logs here, without the sha1 cache of compiled bytecode
  execute_process(COMMAND "${COMPILER}" "${dir}/shaders.blk" -q -shaderOn -nodisassembly -commentPP -codeDumpErr
      -no_sha1_cache -clearBlkHashInDump -o "${dir}/obj" -logdir "${dir}/log"
    WORKING_DIRECTORY "${blk_dir}" RESULT_VARIABLE result OUTPUT_VARIABLE output ERROR_VARIABLE output)
  file(GLOB dumps "${dir}/gui.*.shdump.bin")
  list(LENGTH dumps count)
  if(NOT result EQUAL 0 OR NOT count EQUAL 1)
    message(FATAL_ERROR "compilation ${run} failed (exit code ${result}, dumps: '${dumps}'):\n${output}")
  endif()
  file(SHA256 "${dumps}" hash${run})
endforeach()
if(NOT hash1 STREQUAL hash2)
  message(FATAL_ERROR "the dumps of two compilations of the same shaders differ: ${OUT}/run1, ${OUT}/run2")
endif()
file(COPY_FILE "${dumps}" "${OUT}/gui.shdump.bin")

execute_process(COMMAND "${SHADER_INFO}" "${OUT}/gui.shdump.bin" "-outfile:${OUT}/shaderInfo.txt"
  RESULT_VARIABLE result OUTPUT_VARIABLE output ERROR_VARIABLE output)
if(NOT result EQUAL 0)
  message(FATAL_ERROR "shaderInfo cannot read the dump (exit code ${result}):\n${output}")
endif()
file(READ "${OUT}/shaderInfo.txt" info)
set(expected "Shaders bindump is intact with checksum" "--- shader\\[[0-9]+\\] - gui_default ---"
  "--- shader\\[[0-9]+\\] - imgui ---")
if(NOT STUB)
  list(APPEND expected "imgui_tex_type\\[[0-9]+\\] global" "\\* [1-9][0-9]* vertex shaders"
    "\\* [1-9][0-9]* pixel shaders")
endif()
foreach(regex IN LISTS expected)
  if(NOT info MATCHES "${regex}")
    message(FATAL_ERROR "shaderInfo's summary of the dump (${OUT}/shaderInfo.txt) has no match for '${regex}'")
  endif()
endforeach()
