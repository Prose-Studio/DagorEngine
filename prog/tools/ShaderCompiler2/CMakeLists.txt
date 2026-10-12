# The shader compilers of the CDK (dsc2-<target>): one front end (the dolphin/whale parsers of the shader language,
# semantics, variants, stcode, the dump writer) with a back end per target API:
#   hlsl11 (DX11 bytecode through FXC), dx12 (DXIL through DXC), spirv (Vulkan, through DXC), metal (through DXC and
#   SPIRV-Cross), stub (no bytecode)
# Windows builds them all, Linux spirv and stub, macOS metal and stub. They run with mimalloc, without the memory
# debug checks, outside Dbg (as jam's tools did).
if(WIN32) # the DX12 back end (DXIL, with FXC as the preprocessor)
  add_subdirectory(dx12)
endif()
add_subdirectory(hlsl2spirv)
add_subdirectory(nodeBased)
add_subdirectory(shaderBlobDisassembler)

set(common_sources
  shaderVariantSrc.cpp winmain_con.cpp main.cpp globVarSem.cpp shSemCode.cpp assemblyShader.cpp variablesMerger.cpp
  gatherVar.cpp semUtils.cpp shExpr.cpp shExprParser.cpp shlexterm.cpp shLocVar.cpp shMacro.cpp shsem.cpp sh_stat.cpp
  shCompiler.cpp debugSpitfile.cpp globalConfig.cpp hwSemantic.cpp hwAssembly.cpp shaderSemantic.cpp
  variantSemantic.cpp variantAssembly.cpp preshaderCompilation.cpp gatherVariantLocalVars.cpp
  shCode.cpp shTargetStorage.cpp shAssumes.cpp shaderBytecodeCache.cpp cppStcode.cpp cppStcodeAssembly.cpp
  cppStcodePasses.cpp hlslRegisters.cpp globvar.cpp intervals.cpp samplers.cpp boolVar.cpp boolExpr.cpp
  shaderVariant.cpp shaderSave.cpp shLog.cpp shUtils.cpp shFunc.cpp shCompilationInfo.cpp loadShaders.cpp
  binDumpUtils.cpp makeShBinDump.cpp transcodeShader.cpp namedConst.cpp renderPassObject.cpp framebufferLayout.cpp
  refinedBlockLayout.cpp refinedBlockRegisterAllocator.cpp codeBlocks.cpp condParser.cpp deSerializationContext.cpp
  linkShaders.cpp parser/bparser.cpp gitRunner.cpp processes.cpp
)
if(WIN32)
  list(APPEND common_sources processes_win.cpp)
else()
  list(APPEND common_sources processes_unix.cpp)
endif()
# the predefined declarations of each target, embedded into hwAssembly.cpp
file(GLOB predefines RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS
  "${CMAKE_CURRENT_SOURCE_DIR}/predefines_*.hlsl")

set(common_includes
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${DAGOR_PROG_DIR}/tools/sharedInclude
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
)
if(WIN32)
  list(APPEND common_includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude/breakpad)
endif()
set(common_deps 3rdPartyLibs.eastl engine.osApiWrappers engine.kernel engine.ioSys engine.startup engine.baseUtil
  engine.math engine.perfMon.daProfilerStub engine.perfMon.perfTimerStub 3rdPartyLibs.hash.BLAKE3 tools.libTools.util)
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND common_deps gameLibs.breakpad.binder)
elseif(LINUX)
  list(APPEND common_deps engine.osApiWrappers.messageBox.stub)
endif()
# the memory manager without its debug checks; mimalloc outside Dbg on Windows without ASan
if(WIN32 AND NOT DAGOR_SANITIZE STREQUAL "address")
  list(APPEND common_deps "$<IF:$<CONFIG:Dbg>,engine.memory.default.off,engine.memory.mimalloc.off>")
else()
  list(APPEND common_deps engine.memory.default.off)
endif()
set(common_options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND common_options -Wno-comment -Wno-int-to-pointer-cast -Wno-writable-strings)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND common_options -Wno-write-strings)
endif()
set(dxc_defines BINDUMP_TARGET_BE=0 _CRT_SECURE_NO_DEPRECATE _HAS_EXCEPTIONS=0 _SECURE_SCL=0 EXCLUDE_PSTDINT)

# dsc2_compiler(<name> [DXC [RUNTIME_SUBDIR <dir>]] [SOURCES ...] [PRIVATE_INCLUDES ...] [PRIVATE_DEFINES ...]
#               [COMPILE_OPTIONS ...] [LINK ...]): one shader compiler with the common front end; DXC: with the DXC
#               runtime libraries next to it (in <dir> there)
function(dsc2_compiler name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "DXC" "RUNTIME_SUBDIR" "SOURCES;PRIVATE_INCLUDES;PRIVATE_DEFINES;COMPILE_OPTIONS;LINK")
  dagor_add_executable(${name} LAX ${common_sources} ${arg_SOURCES})
  target_include_directories(${name} PRIVATE ${common_includes} ${arg_PRIVATE_INCLUDES})
  target_compile_definitions(${name} PRIVATE ${arg_PRIVATE_DEFINES})
  target_compile_options(${name} PRIVATE ${common_options} ${arg_COMPILE_OPTIONS})
  target_link_libraries(${name} PRIVATE ${common_deps} ${arg_LINK})
  dagor_target_stringify(${name} ${predefines})
  set_target_properties(${name} PROPERTIES DAGOR_EXCEPTIONS ON)
  dagor_install_cdk(${name})
  dagor_legacy_parsers(${name} LEX shlex.dlp SYN shsyn.whl)
  if(arg_DXC)
    find_package(DXC REQUIRED)
    target_link_libraries(${name} PRIVATE DXC::DXC)
    set(subdir)
    if(arg_RUNTIME_SUBDIR)
      set(subdir SUBDIR "${arg_RUNTIME_SUBDIR}")
    endif()
    dagor_target_runtime_files(${name} ${subdir} ${DXC_RUNTIME_LIBRARIES})
  endif()
endfunction()

# no bytecode at all: the shader dump layout and stcode of any target
set(stub_options)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(stub_options -Wno-switch)
endif()
dsc2_compiler(dsc2-stub
  SOURCES ver_obj_pcdx.cpp
  PRIVATE_DEFINES _CROSS_TARGET_EMPTY BINDUMP_TARGET_BE=0
  COMPILE_OPTIONS ${stub_options}
)

if(WIN32)
  dsc2_compiler(dsc2-hlsl11
    SOURCES hlsl11transcode/asmShaders11.cpp ver_obj_pcdx.cpp
    PRIVATE_DEFINES _CROSS_TARGET_DX11 BINDUMP_TARGET_BE=0
    LINK System::d3dcompiler
  )
  # DXC in dxc-dx12/pc next to it, as the compiler looks for it there
  dsc2_compiler(dsc2-dx12 DXC RUNTIME_SUBDIR dxc-dx12/pc
    SOURCES ver_obj_dxc.cpp
    PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    PRIVATE_DEFINES _CROSS_TARGET_DX12 ${dxc_defines} USE_BINDLESS_FOR_STATIC_TEX
    LINK tools.ShaderCompiler2.dx12
  )
endif()

if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  set(spirv_options)
  if(LINUX AND (CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND NOT MSVC))
    set(spirv_options -Wno-switch -Wno-sometimes-uninitialized)
  endif()
  dsc2_compiler(dsc2-spirv DXC
    SOURCES ver_obj_spirv.cpp
    PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    PRIVATE_DEFINES _CROSS_TARGET_SPIRV ${dxc_defines}
    COMPILE_OPTIONS ${spirv_options}
    LINK tools.ShaderCompiler2.hlsl2spirv 3rdPartyLibs.regExp
  )
endif()

if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Windows)$")
  set(metal_options)
  set(metal_libs)
  if(WIN32)
    set(metal_libs System::d3dcompiler)
  else()
    set(metal_options -Wno-comment -Wno-writable-strings -Wno-int-to-pointer-cast -Wno-switch
      -Wno-tautological-constant-out-of-range-compare -Wno-undefined-bool-conversion -Wno-deprecated-declarations)
  endif()
  dsc2_compiler(dsc2-metal DXC
    SOURCES
      hlsl2metal/HLSL2MetalCommon.cpp hlsl2metal/asmShaderHLSL2Metal.cpp hlsl2spirv/HLSL2SpirvCommon.cpp
      hlsl2metal/spirv2MetalCompiler.cpp hlsl2metal/asmShaderHLSL2MetalDXC.cpp hlsl2metal/hlsl2spirvCompile.cpp
      ver_obj_metal.cpp
    PRIVATE_INCLUDES
      ${DAGOR_PROG_DIR}/3rdPartyLibs/metal
      ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/glslang
      ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
      ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include
      ${CMAKE_CURRENT_SOURCE_DIR}/hlsl2spirv
      ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/smol-v/source
      ${DAGOR_PROG_DIR}/gameLibs/publicInclude
      ${DAGOR_PROG_DIR}/engine/drv/drv3d_Metal
    PRIVATE_DEFINES _CROSS_TARGET_METAL ${dxc_defines} ENABLE_HLSL $<$<NOT:$<PLATFORM_ID:Windows>>:_STD_RTL_MEMORY>
    COMPILE_OPTIONS ${metal_options}
    LINK
      3rdPartyLibs.hash 3rdPartyLibs.vulkan.smol-v 3rdPartyLibs.metal.spirv2Metal 3rdPartyLibs.vulkan.spirv-tools
      gameLibs.folders gameLibs.spirv ${metal_libs}
  )
endif()
