set(dec_src
  apiwrapper.c
  bitpack.c
  decapiwrapper.c
  decinfo.c
  decode.c
  dequant.c
  fragment.c
  huffdec.c
  idct.c
  info.c
  internal.c
  quant.c
  state.c
)
list(TRANSFORM dec_src PREPEND lib/dec/)
set(FILES ${dec_src} lib/enc/encoder_disabled.c)
