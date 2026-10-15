from "%darg/ui_imports.nut" import *

// The overlay UI (settings.blk ui/overlay_ui_script), drawn over the game; the game's own UI goes here too. Outside Rel
// builds it carries the embedded editor (daEditorEmbedded): F12 opens and closes it (Space in it toggles its camera);
// F10 toggles the game's free camera.
let hasEditor = require_optional("daEditorEmbedded") != null
let editor = hasEditor ? require("%daeditor/editor.nut") : null
let { editorIsActive = Watched(false) } = hasEditor ? require("%daeditor/state.nut") : {}

let hint = {
  rendObj = ROBJ_TEXT
  text = "F12 - editor, F10 - free camera"
  hplace = ALIGN_LEFT
  vplace = ALIGN_BOTTOM
  margin = hdpx(10)
  fontFx = FFT_SHADOW
  fontFxColor = 0xA0000000
}

return @() {
  watch = editorIsActive
  size = flex()
  children = [hasEditor && !editorIsActive.get() ? hint : null, editor]
}
