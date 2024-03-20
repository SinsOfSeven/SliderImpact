import os
import glob
import base64
import argparse

def get_user_order(posbuffers):

    choice = input()

    # User entered data before pressing enter
    while choice:
        choice = choice.strip().split(" ")

        if len(choice) > len(posbuffers):
            print("\nERROR: please only enter up to the number of the original mods\n")
            choice = input()
        else:
            try:
                result = []
                choice = [int(x) for x in choice]
                if len(set(choice)) != len(choice):
                    print("\nERROR: please enter each mod number at most once\n")
                    choice = input()
                elif max(choice) >= len(posbuffers):
                    print("\nERROR: selected index is greater than the largest available\n")
                    choice = input()
                elif min(choice) < 0:
                    print("\nERROR: selected index is less than 0\n")
                    choice = input()
                    print()
                else:
                    for x in choice:
                        result.append(posbuffers[x])
                    return result
            except ValueError:
                print("\nERROR: please only enter the index of the mods you want to merge separated by spaces (example: 3 0 1 2)\n")
                choice = input()

    # User didn't enter anything and just pressed enter
    return posbuffers

def main():
    parser = argparse.ArgumentParser(description="Generates a ShapeKey(s) Slider(s)")
    parser.add_argument("-t", "--test", action="store_true", help="Test Argument")
    parser.add_argument("-s","--slider", default=[0.15, 0.5, 0.8, 0.05], action="store", nargs=4, type=float, help="x_size y_size x_offset y_offset")
    parser.add_argument("-scale", "--scale", default=1, type=float, help="Scale value, default is 1")
    parser.add_argument("-text", "--text", action="store_true", help="Generate text files (These are images that you can then modify)")
    parser.add_argument("-title", "--title", action="store_true", help="Generate text file for title")
    parser.add_argument("-a", "--author", action="store_true", help="Generate text file for author")
    parser.add_argument("-o", "--order", action="store_true", help="Custom Order for Sliders (1 0 2)")
    parser.add_argument("-ns", "--noside", action="store_true", help="Disables sidebar")
    parser.add_argument("-cm","--metric", action="store_true", help="Adds red measurement lines")

    args = parser.parse_args()

    if args.test:
        print("test")

    x_size = args.slider[0]
    y_size = args.slider[1]
    x_offset = args.slider[2]
    y_offset = args.slider[3]
    scale = args.scale
    text=args.text
    title = args.title
    author = args.author
    ns = args.noside
    metric = args.metric


    # Define the folder path
    folder_path = os.getcwd()

    # Get Character's Name from Ini's File Name
    file = glob.glob('*.ini')[0]
    charaname = file[:-4]

    # Iterate over the files in the folder
    baseposition = [filename for filename in os.listdir(folder_path) if "base" in filename.lower() 
            or filename.lower().startswith(f'{charaname}Position.'.lower())][0]

    posbuffers = [filename for filename in os.listdir(folder_path) if filename.lower().startswith(f'{charaname}Position'.lower())
            and "base" not in filename.lower() 
            and not filename.lower().startswith(f'{charaname}Position.'.lower())]

    numberoffiles = len(posbuffers)

    if args.order and numberoffiles >= 2:
        for i, posbuffer in enumerate(posbuffers):
            print(f"\t{i}:  {posbuffer}")

        print(
            "\nThis Script will add Sliders using the order listed above (0 is the default the Mod will start with, and it will cycle 0,1,2...)")
        print(
            "If this is fine, please press ENTER. If not, please enter the order you want the script to merge the mods (example: 1 0 2)")
        print("If you enter less than the total number, this Script will only add Sliders to those listed.\n")
        posbuffers = get_user_order(posbuffers)
        numberoffiles = len(posbuffers)


    print(numberoffiles, charaname, posbuffers, baseposition)
    # Read the contents of the file

    with open(file) as file:
        lines = file.readlines()

    modified=False
    verts = 0
    itexists = False
    # Modify the contents
    modified_lines = []
    for line in lines:
        if (line == "[Present]"):
            itexists = True
        if ("draw = " in line):
            print(line[6:].split(',').pop(0))
            verts = line[6:].split(',').pop(0)
        if("GENERATED SLIDERIMPACT" in line):
            modified=True
        if(not modified):
            modified_lines.append(line.strip())  # Example modification: converting text to uppercase
    skip = False
    # Write the modified contents back to the file
    with open(f'{charaname}.ini', "w") as file:
        wait = False
        textureoverrideposition = 9999999
        for i, line in enumerate(modified_lines):
            wait = False

            if line == f'[TextureOverride{charaname}Position]':
                textureoverrideposition = i+3

            if i == textureoverrideposition and line != '$activeForMenu = 1':
                file.write('$activeForMenu = 1\n')

            if (f'[Resource{charaname}Position]' in line):
                skip = True
                linesskipped = 0

            if (skip):
                linesskipped += 1
                if (linesskipped == 5):
                    skip = False
                else:
                    continue

            file.write(line+"\n")

        print(modified)
        file.write(
f"""; #GENERATED SLIDERIMPACT

[Constants]
global $activeForMenu = 1
global $menu = 0
global $hover = 0
global $click = 0
global $size_x = {x_size}
global $off_x = {x_offset}
global $bar = 0.025
global $size_y = {y_size}
global $off_y = {y_offset}
global $num_slider
post $num_slider = {numberoffiles}+1
global $icon_size = 0.04
global $text_y = 0.0165
global $text_x = 0.055
global $reset = 0
global $precise = 0
global $inside = 0
global $number = 0
global $toggleclick = 0
global $scale = {scale}
{"".join([ 
f'''global persist $Key{i+1} = 0
global $bar{i+1}_yo
post $bar{i+1}_yo = {i+1}/$num_slider
''' for i in range(numberoffiles)
])}
Resource{charaname}Position = copy Resource{charaname}PositionBase
post run = CommandListComputeShapeKeys

[Present]
post $activeForMenu = 0
if $activeForMenu == 1
    run = CommandListMenu
    run = CommandListComputeShapeKeys
endif

[CommandListComputeShapeKeys]
cs-u5 = copy Resource{charaname}PositionBase
{''.join([
f'''run = CommandListKey{i + 1}
''' for i in range(numberoffiles)
])}
Resource{charaname}Position = copy cs-u5
; clean up
x88 = 0
cs-u5 = null
cs-t50 = null
cs-t51 = null
{''.join([
f'''[CommandListKey{i+1}]
cs-t50 = copy Resource{charaname}PositionBase
cs-t51 = copy Resource{posbuffers[i][:-4]}
x88 = $Key{i+1}*$scale
run = CustomShaderKeys
''' for i in range(numberoffiles)
])}
[CustomShaderKeys]
;**** SHAPE KEY SHADER ****
;Contributors: Cybertron, SinsOfSeven, DiXiao
cs = resources/ShapeKey.hlsl
dispatch = {verts}, 1, 1
[Resource{charaname}Position]
[Resource{charaname}PositionBase]
type = Buffer
stride = 40
filename = {baseposition}
{''.join([
f'''[Resource{posbuffers[i][:-4]}]
type = Buffer
stride = 40
filename = {posbuffers[i]}
''' for i in range(numberoffiles)
])}
[KeyToggleMenu]
condition = $activeForMenu
key = >
type = toggle
$menu = 1

[KeyClick]
condition = $menu
key = VK_RBUTTON
type = hold
$click = 1

[KeyToggleClick]
condition = $menu
key = VK_RBUTTON
type = hold
$toggleclick = 1

[KeyReset]
condition = $menu
key = ]
type = toggle
$reset = 1

[KeyPrecise]
condition = $menu
key = RIGHT
back = LEFT
type = cycle
$precise = -1,0,1

[KeyHoldHover]
condition = $menu
key = VK_ALT VK_CTRL
type = hold
$hover = 1

[ResourceBarsUI]
filename = resources/slider_bar.png
[ResourceSliderUI]
filename = resources/slider.png
[ResourceSliderUIOn]
filename = resources/slideron.png
{''.join(['''[ResourceBarsSmallUI]
filename = resources/slider_bar_gap.png''' if metric else ''])}
{''.join(['''[ResourceSlidersTitle]
filename = resources/textResourceTitle.png''' if title else ''])}
{''.join(['''[ResourceSlidersAuthor]
filename = resources/textResourceAuthor.png''' if author else ''])}
[ResourceBackgroundUI]
filename = resources/background.png
[ResourceBorderUI]
filename = resources/border.png
{''.join([ 
(f'''[ResourceSliderIcon{i+1}]
filename = resources/Icon{i+1}.png
'''if not ns else '')+(
f'''[ResourceSliderText{i+1}]
filename = resources/textResource{i+1}.png
''' if text else '')for i in range(numberoffiles)
])}
[CustomShaderSliderMenu]
vs = resources/UIElement.hlsl
ps = resources/UIElement.hlsl
blend = ADD SRC_ALPHA INV_SRC_ALPHA
cull = none
topology = triangle_strip
o0 = set_viewport bb
Draw = 4,0

[CommandListBackdrop]
x87 = $size_x
y87 = $size_y
z87 = $off_x
w87 = $off_y
ps-t100 = ResourceBackgroundUI
run = CustomShaderSliderMenu
{''.join([
'''
x87 = $text_x*2.5
y87 = $text_y*2.5
z87 = $off_x+$size_x/2-($text_x*2.5)/2
ps-t100 = ResourceSlidersTitle
run = CustomShaderSliderMenu'''
if title else ''])}
{''.join([
'''
x87 = $text_x
y87 = $text_y
z87 = $off_x+$size_x-$text_x
w87 = $off_y+$size_y-$text_y
ps-t100 = ResourceSlidersAuthor
run = CustomShaderSliderMenu'''
if author else ''])}

ps-t100 = ResourceBorderUI
x87 = 0.001
y87 = $size_y
z87 = $off_x
w87 = $off_y
run = CustomShaderSliderMenu
x87 = 0.001
y87 = $size_y
z87 = $off_x+$size_x
w87 = $off_y
run = CustomShaderSliderMenu
x87 = $size_x
y87 = 0.002
z87 = $off_x
w87 = $off_y
run = CustomShaderSliderMenu
x87 = $size_x
y87 = 0.002
z87 = $off_x
w87 = $off_y+$size_y
run = CustomShaderSliderMenu

{''.join(['''x87 = $icon_size
y87 = $size_y
z87 = $off_x-$icon_size
w87 = $off_y
ps-t100 = ResourceBackgroundUI
run = CustomShaderSliderMenu
ps-t100 = ResourceBorderUI
x87 = $icon_size
y87 = 0.002
z87 = $off_x-$icon_size
w87 = $off_y
run = CustomShaderSliderMenu
x87 = $icon_size
y87 = 0.002
z87 = $off_x-$icon_size
w87 = $off_y+$size_y
run = CustomShaderSliderMenu
x87 = 0.001
y87 = $size_y
z87 = $off_x-$icon_size
w87 = $off_y
run = CustomShaderSliderMenu''' if not ns else ''])}

[CommandListBars]
x87 = $size_x
y87 = $bar
z87 = $off_x
ps-t100 = ResourceBarsUI
run = CustomShaderSliderMenu

{''.join([f''';Draws Linerules on sliders
ps-t100 = ResourceBarsSmallUI
x87 = 0.0015
y87 = $bar
{''.join([f'''z87 = $off_x+($size_x/10)*{i}-(x87/2)
run = CustomShaderSliderMenu
'''for i in range(1,10)])}
''' if metric else ''])}

{''.join([
f'''
[CommandListSlider{i+1}]
local $v = $Key{i+1}
;DRAW CURSOR
x87 = $bar*res_height/res_width
y87 = $bar
z87 = $v*$size_x+$off_x-($bar*res_height/res_width)/2
w87 = $bar{i+1}_yo * $size_y + $off_y
if $inside == 1 && $number == {i+1}
    ps-t100 = ResourceSliderUIOn
else
    ps-t100 = ResourceSliderUI
endif
run = CustomShaderSliderMenu
'''
+(f''';DRAW ICON
x87 = $icon_size
y87 = $icon_size*res_width/res_height
z87 = $off_x-$icon_size
w87 = $bar{i+1}_yo * $size_y + $off_y - ($icon_size/2)
ps-t100 = ResourceSliderIcon{i+1}
run = CustomShaderSliderMenu
''' if not ns else '') for i in range(numberoffiles)
])}
[CommandListMenu]
local $v = 0

if $menu == 1
    run = CommandListBackdrop
{''.join([
f'''    
    w87 = $bar{i+1}_yo * $size_y + $off_y
    run = CommandListBars
    '''
    + (
    f''';DRAW TEXT
    w87=w87+$bar*0.75
    z87=$off_x+($size_x/2)-($text_x/2)
    x87=$text_x
    y87=$text_y
    ps-t100 = ResourceSliderText{i+1}
    run = CustomShaderSliderMenu
    w87=w87-$bar*0.75
    ''' if text else ''
    )
for i in range(numberoffiles)
])}
    if cursor_x > $off_x && cursor_x < $off_x + $size_x && cursor_y > $off_y-$size_y/20 && cursor_y < $off_y+$size_y/10 && $toggleclick == 1
        $off_x = cursor_x-$size_x/2
        $off_y = cursor_y-$size_y/40
    endif
    
    if cursor_x > $off_x && cursor_x < $off_x + $size_x
{''.join([
f'''        if cursor_y > $bar{i+1}_yo * $size_y + $off_y && cursor_y < $bar{i+1}_yo * $size_y + $bar + $off_y
            $inside = 1
            $number = {i+1}
            if $hover || $click
                $v = (cursor_x-$off_x)/$size_x
                $Key{i+1} = $v
            endif
            if $precise !=0 && ($Key{i+1}>0 || $precise>0)
                $Key{i+1} = $Key{i+1} + ($precise/100)
                $precise = 0
            endif

            if $Key{i+1} < 0.01
                $Key{i+1}=0
            endif
        endif
''' for i in range(numberoffiles)
])}
    endif
    $precise = 0
    if $reset == 1
{''.join([
f'''        $Key{i+1} = 0
''' for i in range(numberoffiles)
])}    endif
    $reset = 0
{''.join([
f'''    run = CommandListSlider{i+1}
''' for i in range(numberoffiles)
])}
$inside = 0
endif
;###MENU CODE END
""")
        
    if not os.path.exists('./resources'):
    # Create directory if it doesn't exist
        try:
            os.makedirs('./resources')
        except:
            print('Could not generate Resources Folder.')
        
    GenerateShaderFiles()
    GenerateTextureFiles()
    for i in range(numberoffiles):
        if not ns:
            GenerateIconFiles(i+1)
        if text:
            GenerateTextFiles(i+1)
    if title:
        GenerateTextFiles('Title')
    if author:
        GenerateTextFiles('Author')
    
def GenerateIconFiles(n):
    sucrose = b'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'
    try:
        with open(f'./resources/Icon{n}.png','xb') as png:
            png.write(base64.b64decode(sucrose))
        print(f'Generated Icon{n}.png')
    except FileExistsError:
        print(f'Icon{n}.png already generated.')
    except:
        print('Could not generate resource Images')


def GenerateTextFiles(n):
    # Smh my head, this makes it seem like it can generate the text.
    # This is just a base64 image like in GenerateTextureFiles()
    text = b'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'
    try:
        with open(f'./resources/textResource{n}.png','xb') as png:
            png.write(base64.b64decode(text))
        print(f'Generated Text{n}.png')
    except FileExistsError:
        print(f'textResource{n}.png already generated.')
    except:
        print('Could not generate resource Images')

def GenerateTextureFiles():
    background = b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsEAAA7BAbiRa+0AAAAZSURBVChTY2RgYKgBYpyACUrjBMNBAQMDAIc4AIx6Z46xAAAAAElFTkSuQmCC'
    slider = b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAgSURBVChTY2QAgvr6+v8gGh00NjYyMkHZOMFwUMDAAADrFQQQEUNZYwAAAABJRU5ErkJggg=='
    slider_bar = b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAZSURBVChTY6A9YPwPBFA2VsAEpQcOMDAAAIpJBABdfFRpAAAAAElFTkSuQmCC'
    slider_on = b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAAgSURBVChTY2QAgv/m5v9BNDpgPHmSkQnKxgmGgwIGBgDplQQQKNuzeAAAAABJRU5ErkJggg=='
    border=b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYSURBVBhXY/z//z8DNsAEpTHAYJRgYAAAVtQDDQweRfMAAAAASUVORK5CYII='
    slider_bar_gap=b'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAAlSURBVChTY2xtbWXAB5igNE5AUAHjli1b/kPZWAFhE2jtSAYGADA4BkdTqrIRAAAAAElFTkSuQmCC'

    try:
        try:
            with open('resources/background.png','xb') as png:
                png.write(base64.b64decode(background))
            print('Generated Background Texture')
        except FileExistsError:
            print(f'Background Texture already generated.')
        try:
            with open('resources/slider_bar.png','xb') as png:
                png.write(base64.b64decode(slider_bar))
            print('Generated Slider Bar Icon')
        except FileExistsError:
            print(f'Slider Bar Icon already generated.')
        try:
            with open('resources/slider.png','xb') as png:
                png.write(base64.b64decode(slider))
            print('Generated Slider Icon')
        except FileExistsError:
            print(f'Slider Icons already generated.')
        try:
            with open('resources/slideron.png','xb') as png:
                png.write(base64.b64decode(slider_on))
            print('Generated Slider On Icon')
        except FileExistsError:
            print(f'Slider On Icons already generated.')
        try:
            with open('resources/border.png','xb') as png:
                png.write(base64.b64decode(border))
            print('Generated Border Icon')
        except FileExistsError:
            print(f'Border Icons already generated.')
        try:
            with open('resources/slider_bar_gap.png','xb') as png:
                png.write(base64.b64decode(slider_bar_gap))
            print('Generated Slider Bar Gap Icon')
        except FileExistsError:
            print(f'Slider Bar Gap texture already generated.')
    except:
        print('Could not generate resource Images')

def GenerateShaderFiles():
    try: 
        with open('resources/ShapeKey.hlsl', 'x') as f:
            f.write(
'''// **** SHAPE KEY SHADER ****
// Contributors: Cybertron, SinsOfSeven
// Helpers: DiXiao, Leo, Silent
// https://github.com/SinsOfSeven/SliderImpact/blob/main/ShapeKeys/ShapeKey.hlsl

struct VertexAttributes {
    float3 position;
    float3 normal;
    float4 tangent;
};

RWStructuredBuffer<VertexAttributes> rw_buffer : register(u5);
StructuredBuffer<VertexAttributes> base : register(t50);
StructuredBuffer<VertexAttributes> shapekey : register(t51);

Texture1D<float4> IniParams : register(t120);
#define key IniParams[88].x

[numthreads(1, 1, 1)]
void main(uint3 threadID : SV_DispatchThreadID)
{
    uint i = threadID.x;
    VertexAttributes diff;
    diff.position = shapekey[i].position - base[i].position ;
    diff.normal = shapekey[i].normal - base[i].normal;
    diff.tangent = shapekey[i].tangent - base[i].tangent;
    rw_buffer[i].position += diff.position*key;
    rw_buffer[i].normal += diff.normal*key;
    rw_buffer[i].tangent += diff.tangent*key;
}
''')

    except FileExistsError:
        print(f'Slider Icons already generated.')
    except:
        print('Shapekey Shader already generated.')
    try:
        with open('resources/UIElement.hlsl', 'x') as f:
            f.write(
'''// **** RESPONSIVE UI SHADER ****
// Contributors: SinsOfSeven
// Ispired by VV_Mod_Maker
// https://github.com/SinsOfSeven/SliderImpact/blob/main/ResponsiveUI/draw_2d.hlsl


Texture1D<float4> IniParams : register(t120);

#define SIZE IniParams[87].xy
#define OFFSET IniParams[87].zw

struct vs2ps {
    float4 pos : SV_Position0;
    float2 uv : TEXCOORD1;
};

#ifdef VERTEX_SHADER
void main(
        out vs2ps output,
        uint vertex : SV_VertexID)
{
    float2 BaseCoord,Offset;
    Offset.x = OFFSET.x*2-1;
    Offset.y = (1-OFFSET.y)*2-1;
    BaseCoord.xy = float2((2*SIZE.x),(2*(-SIZE.y)));
    // Not using vertex buffers so manufacture our own coordinates.
    switch(vertex) {
        case 0:
            output.pos.xy = float2(BaseCoord.x+Offset.x, BaseCoord.y+Offset.y);
            output.uv = float2(1,0);
            break;
        case 1:
            output.pos.xy = float2(BaseCoord.x+Offset.x, 0+Offset.y);
            output.uv = float2(1,1);
            break;
        case 2:
            output.pos.xy = float2(0+Offset.x, BaseCoord.y+Offset.y);
            output.uv = float2(0,0);
            break;
        case 3:
            output.pos.xy = float2(0+Offset.x, 0+Offset.y);
            output.uv = float2(0,1);
            break;
        default:
            output.pos.xy = 0;
            output.uv = float2(0,0);
            break;
    };
    output.pos.zw = float2(0, 1);
}
#endif

#ifdef PIXEL_SHADER
Texture2D<float4> tex : register(t100);

void main(vs2ps input, out float4 result : SV_Target0)
{
    uint width, height;
    tex.GetDimensions(width, height);
    if (!width || !height) discard;
    input.uv.y = 1 - input.uv.y;
    result = tex.Load(int3(input.uv.xy * float2(width, height), 0));
}
#endif

''')
    except FileExistsError:
        print('UI Shader already generated.')

# Run Main
main()
