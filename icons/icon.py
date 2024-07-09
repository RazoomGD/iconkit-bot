import logging as log
import re
from enum import Enum
import plistlib
from typing import Tuple, Optional

from PIL import Image, ImageChops, ImageEnhance
from PIL.Image import Transpose, Resampling

from config import PROJECT_ROOT


class IconType(Enum):
    CUBE = ("player", 1, 484)
    SHIP = ("ship", 1, 169)
    BALL = ("player_ball", 1, 118)
    UFO = ("bird", 1, 149)
    WAVE = ("dart", 1, 96)
    ROBOT = ("robot", 1, 68)
    SPIDER = ("spider", 1, 69)
    SWING = ("swing", 1, 43)
    JET = ("jetpack", 1, 5)

class Quality(Enum):
    LOW = ""
    HD = "hd"
    UHD = "uhd"

class Icon:
    def __init__(
            self,
            icon_type: IconType,
            icon_number: int,
            quality: Quality,
            rgb_1: Tuple[int, int, int],
            rgb_2: Tuple[int, int, int],
            has_glow: bool,
            rgb_glow: Optional[Tuple[int, int, int]]=None
    ):
        # basics
        self.icon_type: IconType = icon_type
        if icon_number > icon_type.value[2] or icon_number < icon_type.value[1]:
            raise ValueError(f"invalid icon number: {icon_number} for {icon_type}")
        self.icon_number: int = icon_number
        self.quality: Quality = quality
        # colors
        self.rgb_1 = rgb_1
        self.rgb_2 = rgb_2
        self.rgb_glow = rgb_glow or rgb_2
        self.has_glow = has_glow
        # paths to textures
        num = f"0{icon_number}" if icon_number < 10 else str(icon_number)
        qual = f"{'-' if quality != Quality.LOW else ''}{quality.value}"
        self.path_to_plist: str = f"{PROJECT_ROOT}/icons/textures/{icon_type.value[0]}_{num}{qual}.plist"
        self.path_to_png: str = f"{PROJECT_ROOT}/icons/textures/{icon_type.value[0]}_{num}{qual}.png"


    def build_icon(self) -> Image.Image:
        with open(self.path_to_plist, "rb") as f:
            plist = plistlib.loads(f.read())

        sprites = Image.open(self.path_to_png).convert("RGBA")

        canvas_size_px = {Quality.LOW: 70, Quality.HD: 140, Quality.UHD: 280}[self.quality]

        # Layers: glow(4) -> dome(3) -> secondary(2) -> primary(1) -> extra(0)
        class Layer(Enum):
            GLOW = 4; DOME = 3; SECONDARY = 2; PRIMARY = 1; EXTRA = 0
        # g1-g4 groups - for robot and spider. Common - for remaining game modes
        class Group(Enum):
            COMMON = 0; G1 = 1; G2 = 2; G3 = 3; G4 = 4

        # 5 groups total. Each group has 5 layers. On each layer may be one part
        parts: list[list[Optional[Image.Image]]] = [[None for _ in range(5)] for _ in range(5)]

        def get_group_and_layer(key: str) -> Tuple[Group, Layer]:
            group, layer = re.findall("[^_]*_\d+(_01|_02|_03|_04)?(_2|_3|_glow|_extra)?_001\.png$", key)[0]
            group = {"": Group.COMMON, "_01": Group.G1, "_02": Group.G2, "_03": Group.G3, "_04": Group.G4}[group]
            layer = {"": Layer.PRIMARY, "_2": Layer.SECONDARY, "_3": Layer.DOME, "_extra": Layer.EXTRA, "_glow": Layer.GLOW}[layer]
            return group, layer

        for key in plist['frames'].keys():

            group, layer = get_group_and_layer(key) # groups are only for robot and spider

            if layer == Layer.GLOW and not self.has_glow:
                continue

            frame = plist['frames'][key]

            sprite_offset: list[int]      = eval(frame["spriteOffset"].replace("{", "[").replace("}", "]"))
            texture_rect: list[list[int]] = eval(frame["textureRect"].replace("{", "[").replace("}", "]"))
            texture_rotated: bool         = frame["textureRotated"]

            crop_box = ( # left, upper, right, lower boundaries
                texture_rect[0][0],
                texture_rect[0][1],
                texture_rect[0][0] + (texture_rect[1][0] if not texture_rotated else texture_rect[1][1]),
                texture_rect[0][1] + (texture_rect[1][1] if not texture_rotated else texture_rect[1][0]),
            )

            part = sprites.crop(crop_box)

            color = {
                Layer.EXTRA:     (255, 255, 255),
                Layer.PRIMARY:   self.rgb_1,
                Layer.SECONDARY: self.rgb_2,
                Layer.DOME:      (255, 255, 255),
                Layer.GLOW:      self.rgb_glow,
            } [layer]

            part = ImageChops.multiply( # apply color to texture (I guess, here is how it's done)
                part,
                Image.new("RGBA", part.size, color=color)
            )

            if texture_rotated:
                part = part.transpose(Transpose.ROTATE_90)

            paste_box = ( # upper left point
                (canvas_size_px // 2) - (texture_rect[1][0] // 2) + int(sprite_offset[0]),
                (canvas_size_px // 2) - (texture_rect[1][1] // 2) - int(sprite_offset[1]),
            )

            sized_part = Image.new("RGBA", (canvas_size_px, canvas_size_px), color=(0,0,0,0))
            sized_part.paste(part, paste_box)

            parts[group.value][layer.value] = sized_part

            log.debug(f"Lay: {layer}; Gro: {group}; Key: {key}: {frame}")

        def transform(images: list[Image.Image], move_x_px: int, move_y_px: int, angle_deg: float, scale: float=1, mirror: bool=False) -> list[Image.Image]:
            multiplier = {Quality.LOW: 0.25, Quality.HD: 0.5, Quality.UHD: 1}[self.quality]
            result = []
            for im in images:
                if im:
                    new = Image.new("RGBA", im.size, color=(0, 0, 0, 0))
                    im = im.transpose(Transpose.FLIP_LEFT_RIGHT) if mirror else im
                    im = im.resize((round(im.width * scale), round(im.height * scale)), Resampling.BILINEAR) if scale != 1 else im
                    new.paste(im.rotate(angle_deg, Resampling.BILINEAR), (round(move_x_px * multiplier), round(move_y_px * multiplier)))
                    result.append(new)
                else:
                    result.append(None)
            return result

        def darken(images: list[Image.Image], brightness: float) -> list[Image.Image]:
            result = []
            for i in range(len(images)):
                im = images[i]
                if im and i == Layer.GLOW.value: # ignore glow layer
                    result.append(im)
                elif im:
                    new = ImageEnhance.Brightness(im).enhance(brightness)
                    result.append(new)
                else:
                    result.append(None)
            return result

        # put the parts to the right positions if it is robot or spider
        if self.icon_type == IconType.ROBOT:
            head =       transform(parts[Group.G1.value], 0, -21, 0)
            front_hand = transform(parts[Group.G2.value], -24, 10, -40)
            back_hand =  transform(parts[Group.G2.value], -31, 5, -55)
            front_leg =  transform(parts[Group.G3.value], -18, 30, 45)
            back_leg =   transform(parts[Group.G3.value], -31, 28, 30)
            front_foot = transform(parts[Group.G4.value], 8, 45, 0)
            back_foot =  transform(parts[Group.G4.value], -12, 45, 0)

            back_hand = darken(back_hand, 0.7)
            back_leg =  darken(back_leg, 0.7)
            back_foot = darken(back_foot, 0.7)

            order = (back_leg, back_hand, back_foot, head, front_leg, front_foot, front_hand)

        elif self.icon_type == IconType.SPIDER:
            head =  transform(parts[Group.G1.value], 2, -8, 0)
            leg_1 = transform(parts[Group.G2.value], 75, 52, 0, 0.88, True)
            leg_2 = transform(parts[Group.G2.value], 38, 53, 0, 0.88)
            leg_3 = transform(parts[Group.G2.value], -10,32, 0)
            leg_4 = transform(parts[Group.G3.value], -53, 35, -40)
            shin =  transform(parts[Group.G4.value], -18, 8, 6)

            leg_1 = darken(leg_1, 0.5)
            leg_2 = darken(leg_2, 0.5)

            order = (leg_2, leg_1, shin, leg_4, head, leg_3)

        # finally build this shit
        if self.icon_type in [IconType.ROBOT, IconType.SPIDER]:
            result = None
            glow = None  # as glow layer is always at the bottom
            for group in order:
                for layer in Layer:
                    part = group[layer.value]
                    if part:
                        if layer == Layer.GLOW:
                            glow = Image.alpha_composite(glow, part) if glow is not None else part
                        else:
                            result = Image.alpha_composite(result, part) if result else part
            result = Image.alpha_composite(glow, result) if glow is not None else result
        else:
            if self.icon_type == IconType.UFO: # ufo-s are not centered for some reason
                group = transform(parts[Group.COMMON.value], 0, 30, 0)
            else:
                group = parts[Group.COMMON.value]

            result = None
            for layer in Layer:
                part = group[layer.value]
                if part:
                    result = Image.alpha_composite(result, part) if result else part

        # result.show()
        return result # ooh, that was very big function

# if __name__ == "__main__":
#     log.getLogger().setLevel("DEBUG")
#     icon = Icon(IconType.SPIDER, 20, Qualities.UHD, (255,0,0), (0, 255,0), True, (0, 0, 255))
#     icon.build_icon().show()
