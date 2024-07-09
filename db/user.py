from icons.color import get_color_rgb
from icons.icon import Icon, IconType, Quality


class User:
    def __init__(self, tg_id, gd_username="", gd_account_id=0, cube=1, ship=1, ufo=1, ball=1, wave=1, robot=1, spider=1, swing=1, jet=1, col_1=0, col_2=3, col_glow=None, has_glow=False, dictionary_args: dict=None):
        self.tg_id: int = tg_id
        self.gd_username: str = gd_username
        self.gd_account_id: int = gd_account_id
        self.cube: int = cube
        self.ship: int = ship
        self.ufo: int = ufo
        self.ball: int = ball
        self.wave: int = wave
        self.robot: int = robot
        self.spider: int = spider
        self.swing: int = swing
        self.jet: int = jet
        self.col_1: int = col_1
        self.col_2: int = col_2
        self.col_glow: int = col_glow or col_2
        self.has_glow: bool = has_glow

        if dictionary_args:
            for k, v in dictionary_args.items():
                setattr(self, k, v)

    def get_list_of_icons(self, quality: Quality):
        rgb_1 = get_color_rgb(self.col_1)
        rgb_2 = get_color_rgb(self.col_2)
        rgb_glow = get_color_rgb(self.col_glow)
        return [
            Icon(IconType.CUBE,   self.cube,   quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
            Icon(IconType.SHIP,   self.ship,   quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
            Icon(IconType.BALL,   self.ball,   quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
            Icon(IconType.UFO,    self.ufo,    quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
            Icon(IconType.WAVE,   self.wave,   quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
            Icon(IconType.ROBOT,  self.robot,  quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
            Icon(IconType.SPIDER, self.spider, quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
            Icon(IconType.SWING,  self.swing,  quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
            Icon(IconType.JET,    self.jet,    quality, rgb_1, rgb_2, self.has_glow, rgb_glow),
        ]

    def set_icon_by_type(self, icon_type: IconType, value: int):
        if icon_type == IconType.CUBE:
            self.cube = value
        elif icon_type == IconType.SHIP:
            self.ship = value
        elif icon_type == IconType.UFO:
            self.ufo = value
        elif icon_type == IconType.BALL:
            self.ball = value
        elif icon_type == IconType.WAVE:
            self.wave = value
        elif icon_type == IconType.ROBOT:
            self.robot = value
        elif icon_type == IconType.SPIDER:
            self.spider = value
        elif icon_type == IconType.SWING:
            self.swing = value
        elif icon_type == IconType.JET:
            self.jet = value

    def get_icon_by_type(self, icon_type: IconType, quality: Quality) -> Icon:
        if icon_type == IconType.CUBE:
            return Icon(icon_type, self.cube, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
        elif icon_type == IconType.SHIP:
            return Icon(icon_type, self.ship, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
        elif icon_type == IconType.UFO:
            return Icon(icon_type, self.ufo, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
        elif icon_type == IconType.BALL:
            return Icon(icon_type, self.ball, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
        elif icon_type == IconType.WAVE:
            return Icon(icon_type, self.wave, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
        elif icon_type == IconType.ROBOT:
            return Icon(icon_type, self.robot, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
        elif icon_type == IconType.SPIDER:
            return Icon(icon_type, self.spider, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
        elif icon_type == IconType.SWING:
            return Icon(icon_type, self.swing, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
        elif icon_type == IconType.JET:
            return Icon(icon_type, self.jet, quality, get_color_rgb(self.col_1), get_color_rgb(self.col_2), self.has_glow, get_color_rgb(self.col_glow))
