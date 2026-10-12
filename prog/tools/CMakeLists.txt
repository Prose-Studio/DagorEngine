# the dirs of prog/tools: the tools' libraries (the games' embedded editor and vromfs packing use some), the Python
# tools' tests, and the programs of the tool variants
add_subdirectory(libTools)
add_subdirectory(hostGuard)
add_subdirectory(pythonCommon)
if(DAGOR_VARIANT MATCHES "^(cdk|editor|maxplug|dargbox)$")
  add_subdirectory(FontGenerator)
  add_subdirectory(ShaderCompiler2)
  add_subdirectory(consoleSq)
  add_subdirectory(converters)
  add_subdirectory(sceneTools)
  add_subdirectory(shaderInfo)
endif()
