from "%darg/ui_imports.nut" import *

let fillerBlock = {
  rendObj = ROBJ_SOLID
  size = const [flex(), sh(1)]
  color = 0xFFFCC66
}

let image = {
  rendObj = ROBJ_IMAGE
  image = Picture("ui/ca_cup1")
  keepAspect = KEEP_ASPECT_FIT
}

return {
  size = const [sh(40), flex()]
  hplace = ALIGN_CENTER
  rendObj = ROBJ_FRAME
  gap = fillerBlock
  flow = FLOW_VERTICAL
  clipChildren = true
  children = [
    // keeps its own size in pixels
    image.__merge({ size = SIZE_TO_CONTENT })
    // fills the available space, keeping the aspect inside it
    image.__merge({ size = flex() })
    // fills the width, the height follows the aspect
    image.__merge({ size = FLEX_H })
    // a fixed width, the height follows the aspect
    image.__merge({ size = const [sh(20), SIZE_TO_CONTENT] })
  ]
}
