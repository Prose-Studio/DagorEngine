# dag4blend, the Blender add-on of the DAG format: the zip Blender installs (__build_pack.py), into
# tools/dagor_cdk/universal with the cdk install
file(GLOB_RECURSE sources CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*")
list(FILTER sources EXCLUDE REGEX "\\.(zip|pyc|bak|blend1)$|/__pycache__/|^${CMAKE_CURRENT_SOURCE_DIR}/(tests|additional)/")
set(zip "${CMAKE_CURRENT_BINARY_DIR}/dag4blend.zip")
add_custom_command(OUTPUT "${zip}"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/__build_pack.py" "${zip}"
  DEPENDS ${sources} "${DAGOR_PROG_DIR}/tools/pythonCommon/pyparsing.py" "${DAGOR_PROG_DIR}/tools/pythonCommon/datablock.py"
  COMMENT "Packing the dag4blend add-on"
  VERBATIM)
add_custom_target(dag4blend DEPENDS "${zip}")
set_property(TARGET dag4blend PROPERTY FOLDER "tools")
install(FILES "${zip}" DESTINATION tools/dagor_cdk/universal COMPONENT cdk OPTIONAL)
