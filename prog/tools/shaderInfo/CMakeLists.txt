# shaderInfo: inspects shader dumps (variables, blocks, bytecode disassembly; AMD's Radeon GPU Analyzer statistics when
# RDTS_ROOT points to a Radeon Developer Tool Suite)
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.lib3d engine.drv.drv3d_null engine.drv.shadersMetaData gameLibs.shaderBlobUnpack 3rdPartyLibs.eastl
  3rdPartyLibs.hash.BLAKE3 engine.shaders engine.perfMon.daProfilerStub tools.ShaderCompiler2.shaderBlobDisassembler
  tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()
set(libs)
if(WIN32)
  list(APPEND libs System::d3dcompiler)
endif()

dagor_add_target(NAME shaderInfo EXECUTABLE LAX
  FILES_CMAKE shaderInfo_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/shaders ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/tools/ShaderCompiler2/shaderBlobDisassembler/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  COMPILE_DEFINITIONS PRIVATE SET_DEFAULT_MAX_SHVARS=8192
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
  CDK
)
if(WIN32)
  # DXIL disassembly loads DXC (shaderBlobDisassembler): its runtime next to the program
  find_package(DXC REQUIRED)
  dagor_target_runtime_files(shaderInfo ${DXC_RUNTIME_LIBRARIES})
endif()

# the tests (tests/), on the GUI shader dumps of the compilers' tests (their fixtures): the bytecode's disassembly
# (shaderBlobDisassembler: DXBC by the D3D compiler, DXIL by the DXC next to the tools, SPIR-V by spirv-tools; none for
# Metal) and the refusal of a dump whose checksum does not match
if(DAGOR_CDK_TESTS)
  set(dumps ${CMAKE_BINARY_DIR}/test-artifacts)
  foreach(check "dx11|dsc2-hlsl11|ps_4_0" "dx12|dsc2-dx12|dx\\.op\\." "spirv|dsc2-spirv|OpEntryPoint Fragment")
    string(REPLACE "|" ";" check "${check}")
    list(POP_FRONT check api compiler expect)
    if(NOT TARGET ${compiler})
      continue()
    endif()
    dagor_add_exec_test(shaderInfo.disasm_${api} COMMAND ${CMAKE_COMMAND} -DSHADER_INFO=$<TARGET_FILE:shaderInfo>
      -DDUMP=${dumps}/${compiler}.gui_shaders/gui.shdump.bin -DOUT=${dumps}/shaderInfo.disasm_${api}
      "-DEXPECT=${expect}" -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/disasm.cmake TAGS cdk TIMEOUT 60)
    set_tests_properties(shaderInfo.disasm_${api} PROPERTIES FIXTURES_REQUIRED ${compiler}.gui_shaders)
  endforeach()
  dagor_add_exec_test(shaderInfo.corrupt_dump COMMAND ${CMAKE_COMMAND} -DSHADER_INFO=$<TARGET_FILE:shaderInfo>
    -DDUMP=${dumps}/dsc2-stub.gui_shaders/gui.shdump.bin -DOUT=${dumps}/shaderInfo.corrupt_dump
    -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/corrupt_dump.cmake TAGS cdk TIMEOUT 60)
  set_tests_properties(shaderInfo.corrupt_dump PROPERTIES FIXTURES_REQUIRED dsc2-stub.gui_shaders)
endif()
