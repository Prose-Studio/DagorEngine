# TODO(jam): KernelLinkage = dynamic ;
# TODO(jam): BuildingTools = yes ;
# TODO(jam): Dependencies = $(Root)/$(Location)/HeightmapLand/jamfile $(Root)/$(Location)/StaticGeom/jamfile
#   $(Root)/$(Location)/IvyGen/jamfile $(Root)/$(Location)/Occluders/jamfile
#   $(Root)/$(Location)/csg/jamfile $(Root)/$(Location)/GraphEditor/jamfile ;
# TODO(jam): editor_jam = $(Root)/$(Location)/jamfile-editor ;
# TODO(jam): platform on $(editor_jam:G=JAM) = -sPlatform=$(Platform) -sPlatformArch=$(PlatformArch)
#   -sCPPStd=$(CPPStd) ;
# TODO(jam): BuildJams = $(editor_jam) ;

dagor_add_target(NAME DaEditor3_all STATIC LAX)
