# cmake -DCOMPILER=<dsc2-*> -DINCLUDE_DIR=<prog/gameLibs/render/shaders> -DOUT=<dir> [-DSTUB=ON] -P errors.cmake
# Broken shaders must fail the compilation, with no dump, and the error where it is: a statement of a shader block
# missing its ; (the front end's parser) and, unless STUB (the stub compiler, which compiles no HLSL), an undeclared
# identifier in a pixel shader (the HLSL compiler's error). INCLUDE_DIR: the engine's shader includes, which every
# shader gets (assert.dshl).
foreach(var COMPILER INCLUDE_DIR OUT)
  if(NOT ${var})
    message(FATAL_ERROR "usage: cmake -DCOMPILER=<dsc2-*> -DINCLUDE_DIR=<prog/gameLibs/render/shaders> -DOUT=<dir> "
      "[-DSTUB=ON] -P errors.cmake")
  endif()
endforeach()
file(REMOVE_RECURSE "${OUT}")

# expect_error(<name> <expected output regex> <shader source>)
function(expect_error name regex source)
  set(dir "${OUT}/${name}")
  file(WRITE "${dir}/${name}.dshl" "${source}")
  file(WRITE "${dir}/shaders.blk" "incDir:t=\"${INCLUDE_DIR}\"\nsource { file:t=\"${dir}/${name}.dshl\" }\n"
    "Compile { fsh:t=5.0 }\noutDumpName:t=\"${dir}/out\"\n")
  execute_process(COMMAND "${COMPILER}" "${dir}/shaders.blk" -q -shaderOn -nodisassembly -no_sha1_cache
      -o "${dir}/obj" -logdir "${dir}/log"
    WORKING_DIRECTORY "${dir}" RESULT_VARIABLE result OUTPUT_VARIABLE output ERROR_VARIABLE output)
  file(GLOB dumps "${dir}/out.*")
  if(result EQUAL 0 OR dumps OR NOT output MATCHES "${regex}")
    message(FATAL_ERROR "${name}: the compilation must fail with no dump (exit code ${result}, dumps: '${dumps}') and "
      "match '${regex}':\n${output}")
  endif()
endfunction()

expect_error(syntax_error "syntax_error\\.dshl\\(6,3\\): syntax: unexpected <z_write>" [[
shader syntax_error
{
  cull_mode = none;
  z_test = false
  // the statement above misses its ;
  z_write = false;
}
]])

if(NOT STUB)
  set(regex "hlsl_error\\.dshl\\(12,[0-9]+\\): compile\\(ps_5_0, error_ps\\) failed")
  string(APPEND regex ".*undeclared identifier 'undefined_value'")
  expect_error(hlsl_error "${regex}" [[
shader hlsl_error
{
  cull_mode = none;
  hlsl(vs) {
    float4 error_vs(uint id : SV_VertexID) : SV_Position { return float4(0, 0, 0, 1); }
  }
  hlsl(ps) {
    // a value it never declares
    float4 error_ps() : SV_Target { return undefined_value; }
  }
  compile("target_vs", "error_vs");
  compile("target_ps", "error_ps");
}
]])
endif()
