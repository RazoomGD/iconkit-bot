from PIL import Image

from config import PROJECT_ROOT
from icons.icon import Icon, Quality


# puts icons from the list on a gray horizontal bar
def create_icon_bar(icons: list[Icon]):
    bar_file = {Quality.LOW: "icon_bar_01.png", Quality.HD: "icon_bar_01-hd.png", Quality.UHD: "icon_bar_01-uhd.png"}[icons[0].quality]

    icons = [icon.build_icon() for icon in icons]
    base_width, base_height = icons[0].width, icons[0].height # depends on quality
    boxes = [icon.getbbox() for icon in icons]
    # crop empty areas of images and calculate shifted center coordinates
    cropped_icons_with_center_coords = [(icons[i].crop(boxes[i]), base_width//2-boxes[i][0], base_height//2-boxes[i][1]) for i in range(len(icons))]

    bar = Image.open(f"{PROJECT_ROOT}/icons/textures/templates/{bar_file}").convert("RGBA")
    center = [round(bar.width*(0.95/len(icons)+0.05)/2), bar.height//2] # complex math
    offset = round(bar.width*0.95/len(icons))

    base = Image.new("RGBA", (bar.width, bar.height), (0,0,0,0))
    for icon, cx, cy in cropped_icons_with_center_coords:
        base.paste(icon, box=(center[0]-cx, center[1]-cy))
        center[0] += offset

    return Image.alpha_composite(bar, base)


# puts icons from the list on a grid of 2 rows
def create_icon_grid(icons: list[Icon]):
    bar_file = {Quality.LOW: "icon_bar_02.png", Quality.HD: "icon_bar_02-hd.png", Quality.UHD: "icon_bar_02-uhd.png"}[icons[0].quality]

    icons = [icon.build_icon() for icon in icons]

    base_width, base_height = icons[0].width, icons[0].height # depends on quality
    boxes = [icon.getbbox() for icon in icons]
    # crop empty areas of images and calculate shifted center coordinates
    cropped_icons_with_center_coords = [(icons[i].crop(boxes[i]), base_width//2-boxes[i][0], base_height//2-boxes[i][1]) for i in range(len(icons))]

    bar = Image.open(f"{PROJECT_ROOT}/icons/textures/templates/{bar_file}").convert("RGBA")
    center = [round(bar.width*0.12), round(bar.height*0.2625)]
    offset = round(bar.width*0.19)

    base = Image.new("RGBA", (bar.width, bar.height), (0,0,0,0))

    for i in range(min(5, len(icons))):
        icon, cx, cy = cropped_icons_with_center_coords[i]
        base.paste(icon, box=(center[0]-cx, center[1]-cy))
        center[0] += offset

    center = [round(bar.width*0.215), round(bar.height*0.7375)]

    for i in range(5, len(icons)):
        icon, cx, cy = cropped_icons_with_center_coords[i]
        base.paste(icon, box=(center[0]-cx, center[1]-cy))
        center[0] += offset

    return Image.alpha_composite(bar, base)

# puts a single icon into a square
def create_icon_square(icon: Icon):
    image = icon.build_icon()
    center = (image.width//2, image.height//2)
    square_file = {Quality.LOW: "icon_square_01.png", Quality.HD: "icon_square_01-hd.png", Quality.UHD: "icon_square_01-uhd.png"}[icon.quality]
    square = Image.open(f"{PROJECT_ROOT}/icons/textures/templates/{square_file}").convert("RGBA")
    base = Image.new("RGBA", square.size, (0,0,0,0))
    base.paste(image, (base.width//2-center[0], base.height//2-center[1]))
    return Image.alpha_composite(square, base)

