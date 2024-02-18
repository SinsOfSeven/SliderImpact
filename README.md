# SliderImpact (WIP)

[Shape Keys Shader](#shape-keys-shader)

[Menu Shader](#menu-shader)

## Shape Keys Shader
Use Example
```ini
[CommandListComputeShapeKeys]
Resource\Shape\Key = copy ResourcePosition.Base
; 1st Key
cs-t50 = copy ResourcePosition.Base
cs-t51 = copy ResourcePosition.1
x88 = $Key1
$\Shape\KeyBatch = 58742
run = CustomShader\Shape\Keys
; 2nd Key
cs-t50 = copy ResourcePosition.Base
cs-t51 = copy ResourcePosition.2
x88 = $Key2
$\Shape\KeyBatch = 58742
run = CustomShader\Shape\Keys
```

## Menu Shader
Use Example
```ini
[CommandListCursors.2]
;NORMALIZE VAR
local $v = (($Key2+1)/2)
;DRAW CURSOR
x5 = $bar_y*res_height/res_width
y5 = $bar_y
z5 = $v*$bar_x+$bar_xo-($bar_y*res_height/res_width)/2
w5 = $bar2_yo
ps-t100 = ResourceCursor2
run = CustomShaderMenu\Element
;DRAW ICON
x5 = $icon_size
y5 = $icon_size*res_width/res_height
z5 = $bar_xo-$icon_size
w5 = $bar2_yo
ps-t100 = ResourceSliderIcon2
run = CustomShaderMenu\Element
```