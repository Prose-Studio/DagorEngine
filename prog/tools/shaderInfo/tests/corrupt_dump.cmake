# cmake -DSHADER_INFO=<shaderInfo> -DDUMP=<shader dump> -DOUT=<dir> -P corrupt_dump.cmake
# A copy of the dump with a byte appended no longer matches the checksum in its header: shaderInfo must refuse to load
# it (the engine's loader stops with a fatal error) instead of reading the data.
foreach(var SHADER_INFO DUMP OUT)
  if(NOT ${var})
    message(FATAL_ERROR "usage: cmake -DSHADER_INFO=<shaderInfo> -DDUMP=<shader dump> -DOUT=<dir> "
      "-P corrupt_dump.cmake")
  endif()
endforeach()
file(REMOVE_RECURSE "${OUT}")
file(MAKE_DIRECTORY "${OUT}")
file(COPY_FILE "${DUMP}" "${OUT}/corrupt.shdump.bin")
file(APPEND "${OUT}/corrupt.shdump.bin" "!")
execute_process(COMMAND "${SHADER_INFO}" "${OUT}/corrupt.shdump.bin" "-outfile:${OUT}/shaderInfo.txt"
  RESULT_VARIABLE result OUTPUT_VARIABLE output ERROR_VARIABLE output)
set(log "")
if(EXISTS "${OUT}/shaderInfo.txt")
  file(READ "${OUT}/shaderInfo.txt" log)
endif()
if(result EQUAL 0 OR NOT log MATCHES "checksum validation failed")
  message(FATAL_ERROR "shaderInfo did not reject the corrupt dump (exit code ${result}, see ${OUT}/shaderInfo.txt):\n"
    "${output}")
endif()
