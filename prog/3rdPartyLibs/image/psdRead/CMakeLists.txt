# Adobe Photoshop PSD reader (M. Scott Heiman's, modified for Dagor)
set(sources psd.cpp bmgImage.cpp)

dagor_add_library(3rdPartyLibs.image.psdRead LAX ${sources})
