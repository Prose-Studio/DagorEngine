# The Dagor Engine: its libraries, tools and unit tests, in the variant the preset names (DAGOR_VARIANT; see
# CMakePresets.json, cmake --list-presets). Games are projects of their own whose trees add this directory through
# find_package(Dagor) (cmake/DagorConfig.cmake): there it is a subproject that builds what the game links.
cmake_minimum_required(VERSION 4.0)
project(DagorEngine LANGUAGES C CXX)
include(cmake/Dagor.cmake)

add_subdirectory(3rdPartyLibs)
add_subdirectory(1stPartyLibs)
add_subdirectory(engine)
add_subdirectory(commonFx)
add_subdirectory(gameLibs)
add_subdirectory(daNetGameLibs)
add_subdirectory(tools)
if(DAGOR_VARIANT MATCHES "^(game|editor)$")
  add_subdirectory(daNetGame)
endif()
if(DAGOR_DAS_AOT_COMPILER)
  add_subdirectory(daNetGame-das-aot)
endif()

# the programs of the variant's default build (cmake --build --preset <host>-<variant>); the test programs are the
# tests variant's (DagorTesting.cmake)
if(NOT PROJECT_IS_TOP_LEVEL)
  return()
endif()
if(DAGOR_VARIANT STREQUAL "cdk")
  # the CDK: the command-line tools of the content pipeline (shader compilers, packers, converters) on the static
  # kernel, and the GUI shaders of the tools; the data the tools load that is not built is installed with them
  dagor_build_by_default(dolphin whale duktape csq ddsConverter ddsx2dds ddsxCvt guiTex fontgen2 pcDdsxConv iosDdsxConv
    andDdsxConv csvUtil2 dbldUtil dumpGrp resCleanUtil resDiffUtil resUpd binBlk vromfsPacker shaderInfo dsc2-stub
    dsc2-nodeBased)
  foreach(platform_tool dsc2-hlsl11 dsc2-dx12 dsc2-spirv dsc2-metal guiShaders-dx11 guiShaders-dx12 guiShaders-spirv
                        guiShaders-metal)
    if(TARGET ${platform_tool})
      dagor_build_by_default(${platform_tool})
    endif()
  endforeach()
  install(DIRECTORY tools/toolsData/ DESTINATION tools COMPONENT cdk PATTERN README.md EXCLUDE)
elseif(DAGOR_VARIANT STREQUAL "assets")
  # the tools on the shared kernel (daKernel): daBuild with its exporter plugins, ddsxCvt2
  dagor_build_by_default(tools.libTools.daKernel daBuild daBuild-job a2dExp animCharExp collisionExp fastPhysExp fxExp
    impostorExp landClsExp locShadersExp matExp modelExp phObjExp texExp compositRefProv efxRefProv splineRefProv
    vehicleExp ddsxCvt2)
elseif(DAGOR_VARIANT STREQUAL "editor")
  # the GUI editors on the shared kernel: daEditor3x with its plugins, AssetViewer, impostorBaker, blkEditor, plodGen
  dagor_build_by_default(tools.libTools.daKernel daEditor3x staticGeom ivyGen occluders graphEditor csg heightmapLand
    heightmapLand-aces assetViewer2 impostorBaker plodGen)
  if(TARGET blkEditor) # Windows
    dagor_build_by_default(blkEditor)
  endif()
elseif(DAGOR_VARIANT STREQUAL "dargbox")
  dagor_build_by_default(dargbox)
elseif(DAGOR_VARIANT STREQUAL "maxplug" AND TARGET dagor) # the plugin, where the Max SDK is there
  dagor_build_by_default(dagor)
endif()
