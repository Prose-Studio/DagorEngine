# Open Asset Import Library (assimp): the importers of OBJ, FBX, Collada, glTF 2 (with Draco meshes) and 3DS and the
# post-processing steps, no exporters; zip archives through unzip, XML through pugixml, JSON through rapidjson.
# Exceptions and RTTI are on whatever the tree's settings: the importers report errors with exceptions, and the FBX and
# STEP ones dispatch on dynamic_cast.

# the importers left out
set(disabled X AMF MD3 MDL MD2 PLY ASE HMP SMD MDC MD5 STL LWO DXF NFF RAW SIB OFF AC BVH IRRMESH IRR Q3D B3D TERRAGEN
  CSM 3D LWS OGRE OPENGEX MS3D COB BLEND Q3BSP NDO IFC XGL ASSBIN GLTF1 C4D 3MF X3D MMD M3D IQM)
list(TRANSFORM disabled PREPEND ASSIMP_BUILD_NO_)
list(TRANSFORM disabled APPEND _IMPORTER)
set(options)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-implicit-const-int-float-conversion) # draco/attributes/geometry_attribute.h
endif()

dagor_add_target(NAME 3rdPartyLibs.assimp STATIC LAX
  FILES_CMAKE assimp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    . code include ${DAGOR_PROG_DIR}/3rdPartyLibs/pugixml ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/unzip ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  COMPILE_DEFINITIONS PRIVATE
    ASSIMP_BUILD_NO_OWN_ZLIB RAPIDJSON_HAS_STDSTRING ASSIMP_BUILD_NO_EXPORT ${disabled} ASSIMP_FBX_USE_PAGE_ALLOCATOR
    ASSIMP_ENABLE_DRACO
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.arc.unzip 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.pugixml 3rdPartyLibs.eastl 3rdPartyLibs.draco
  PROPERTIES DAGOR_EXCEPTIONS ON DAGOR_RTTI ON
)
