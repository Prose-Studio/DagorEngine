# The Vulkan driver (Windows, Linux, Android), with FSR upscaling on x64 (3rdPartyLibs/fsr3.1) and the RenderDoc
# capture module outside Rel; DLSS and XeSS have their stubs (the fork has neither SDK).
set(dev "$<NOT:$<CONFIG:Rel>>")
set(dir ${CMAKE_CURRENT_SOURCE_DIR})
set(defines INSIDE_DRIVER)
if(DAGOR_STREAMLINE)
  list(APPEND defines HAS_STREAMLINE)
endif()
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode
  ${DAGOR_PROG_DIR}/engine/drv/drv3d_vulkan
  ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/smol-v/source
  ${DAGOR_PROG_DIR}/3rdPartyLibs/vulkan/spirv-tools/include
  ${DAGOR_PROG_DIR}/dagorInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui
  ${DAGOR_PROG_DIR}/3rdPartyLibs/imgui-node-editor
)
# jam linked engine/imgui's stub in Rel; its programs all link engine/imgui, whose objects came first in jam's order
set(deps engine.drv.drv3d_commonCode engine.drv.shadersMetaData.spirv 3rdPartyLibs.vulkan.smol-v engine.imgui)
list(APPEND deps "$<${dev}:3rdPartyLibs.imgui-node-editor>")
set(libs)
if(WIN32)
  list(APPEND libs System::wintrust)
  find_package(NVAPI)
  if(TARGET NVAPI::NVAPI)
    list(APPEND deps NVAPI::NVAPI)
  endif()
elseif(LINUX)
  list(APPEND deps engine.osApiWrappers.linuxGUI)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Windows)$" AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/fsr3.1/include)
endif()

dagor_add_target(NAME engine.drv.drv3d_vulkan STATIC
  FILES_CMAKE drv3d_vulkan_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
  FORCE_INCLUDES ${dir}/d3d/config.h ${dir}/driver_defs.h
)
