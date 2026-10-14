# cmake -DSHADER_INFO=<shaderInfo> -DDUMP=<shader dump> -DOUT=<dir> -DEXPECT=<regex> -P disasm.cmake
# shaderInfo disassembles the bytecode of the dump (-disasm, through shaderBlobDisassembler): the disassembly must have
# a match for EXPECT, which only the API's disassembler writes.
foreach(var SHADER_INFO DUMP OUT EXPECT)
  if(NOT ${var})
    message(FATAL_ERROR "usage: cmake -DSHADER_INFO=<shaderInfo> -DDUMP=<shader dump> -DOUT=<dir> -DEXPECT=<regex> "
      "-P disasm.cmake")
  endif()
endforeach()
file(REMOVE_RECURSE "${OUT}")
file(MAKE_DIRECTORY "${OUT}")
execute_process(COMMAND "${SHADER_INFO}" "${DUMP}" -disasm "-outfile:${OUT}/disasm.txt"
  RESULT_VARIABLE result OUTPUT_VARIABLE output ERROR_VARIABLE output)
if(NOT result EQUAL 0 OR NOT EXISTS "${OUT}/disasm.txt")
  message(FATAL_ERROR "shaderInfo -disasm failed (exit code ${result}, see ${OUT}/disasm.txt):\n${output}")
endif()
file(READ "${OUT}/disasm.txt" disasm)
if(NOT disasm MATCHES "${EXPECT}")
  message(FATAL_ERROR "the disassembly of ${DUMP} (${OUT}/disasm.txt) has no match for '${EXPECT}'")
endif()
