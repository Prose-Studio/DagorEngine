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

# dsc2_compiler(NAME <name> [DXC [RUNTIME_SUBDIR <dir>]] <dagor_add_target arguments>): one shader compiler of the CDK,
# the common front end (ShaderCompiler2_files.cmake) with the target's back end; DXC: with the DXC runtime libraries
# next to it (in <dir> there)
function(dsc2_compiler)
  cmake_parse_arguments(PARSE_ARGV 0 arg "DXC" "NAME;RUNTIME_SUBDIR" "")
  set(name ${arg_NAME})
  dagor_add_target(NAME ${name} EXECUTABLE LAX CDK ${arg_UNPARSED_ARGUMENTS}
    FILES_CMAKE ShaderCompiler2_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${common_includes}
    COMPILE_OPTIONS PRIVATE ${common_options}
    BUILD_DEPENDENCIES PRIVATE ${common_deps}
    PROPERTIES DAGOR_EXCEPTIONS ON
  )
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
dsc2_compiler(NAME dsc2-stub
  FILES_CMAKE dsc2-stub_files.cmake
  COMPILE_DEFINITIONS PRIVATE _CROSS_TARGET_EMPTY BINDUMP_TARGET_BE=0
  COMPILE_OPTIONS PRIVATE ${stub_options}
)

if(WIN32)
  dsc2_compiler(NAME dsc2-hlsl11
    FILES_CMAKE dsc2-hlsl11_files.cmake
    COMPILE_DEFINITIONS PRIVATE _CROSS_TARGET_DX11 BINDUMP_TARGET_BE=0
    BUILD_DEPENDENCIES PRIVATE System::d3dcompiler
  )
  # DXC in dxc-dx12/pc next to it, as the compiler looks for it there
  dsc2_compiler(NAME dsc2-dx12 DXC RUNTIME_SUBDIR dxc-dx12/pc
    FILES_CMAKE dsc2-dx12_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    COMPILE_DEFINITIONS PRIVATE _CROSS_TARGET_DX12 ${dxc_defines} USE_BINDLESS_FOR_STATIC_TEX
    BUILD_DEPENDENCIES PRIVATE tools.ShaderCompiler2.dx12
  )
endif()

if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$")
  set(spirv_options)
  if(LINUX AND (CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND NOT MSVC))
    set(spirv_options -Wno-switch -Wno-sometimes-uninitialized)
  endif()
  dsc2_compiler(NAME dsc2-spirv DXC
    FILES_CMAKE dsc2-spirv_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    COMPILE_DEFINITIONS PRIVATE _CROSS_TARGET_SPIRV ${dxc_defines}
    COMPILE_OPTIONS PRIVATE ${spirv_options}
    BUILD_DEPENDENCIES PRIVATE tools.ShaderCompiler2.hlsl2spirv 3rdPartyLibs.regExp
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
  dsc2_compiler(NAME dsc2-metal DXC
    FILES_CMAKE dsc2-metal_files.cmake
    INCLUDE_DIRECTORIES PRIVATE
      ${DAGOR_PROG_DIR}/3rdPartyLibs/metal ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/glslang
      ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include
      ${CMAKE_CURRENT_SOURCE_DIR}/hlsl2spirv ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/smol-v/source
      ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/engine/drv/drv3d_Metal
    COMPILE_DEFINITIONS PRIVATE
      _CROSS_TARGET_METAL ${dxc_defines} ENABLE_HLSL $<$<NOT:$<PLATFORM_ID:Windows>>:_STD_RTL_MEMORY>
    COMPILE_OPTIONS PRIVATE ${metal_options}
    BUILD_DEPENDENCIES PRIVATE
      3rdPartyLibs.hash 3rdPartyLibs.vulkan.smol-v 3rdPartyLibs.metal.spirv2Metal 3rdPartyLibs.vulkan.spirv-tools
      gameLibs.folders gameLibs.spirv ${metal_libs}
  )
endif()
