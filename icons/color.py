from typing import Tuple

# 0 - 106
colors = {51: 'fdd4ce', 19: 'ff7d7d', 48: 'ff3a3a', 9: 'ff0000', 62: 'ffb972', 63: 'ffa040', 10: 'ff7d00', 29: 'ff4b00', 70: 'ffffc0', 42: 'fffa7f', 11: 'ffff00', 27: '7d7d00', 72: 'c0ffa0', 73: 'b1ff6d', 0: '7dff00', 1: '00ff00', 37: '960000', 53: '700000', 54: '520200', 55: '380106', 26: 'af4b00', 59: 'a36246', 60: '754936', 61: '563528', 71: 'fde0a0', 14: 'ffb900', 31: '966400', 45: '50320e', 105: 'd2ff32', 28: '4baf00', 32: '649600', 20: '00af4b', 25: 'af004b', 56: '804f4f', 57: '7a3535', 58: '512424', 30: '963200', 64: '66311e', 65: '5b2700', 66: '472000', 46: 'cda576', 67: 'a77b4d', 68: '6d5339', 69: '513e2a', 2: '00ff7d', 38: '009600', 79: '006000', 80: '004000', 74: 'c0ffe0', 75: '94ffe4', 44: '00ffc0', 3: '00ffff', 83: 'a0ffff', 16: '00c8ff', 4: '007dff', 5: '0000ff', 52: 'beb5ff', 41: '7d7dff', 6: '7d00ff', 35: '640096', 98: 'fcb5ff', 8: 'ff007d', 36: '960064', 103: '66033e', 40: '7dffaf', 76: '43a18a', 77: '316d5f', 78: '265449', 22: '004baf', 39: '000096', 84: '010770', 50: '000a4c', 47: 'b680ff', 23: '4b00af', 92: '3d068c', 93: '370860', 7: 'ff00ff', 13: 'b900ff', 24: '7d007d', 104: '470134', 33: '009664', 21: '007d7d', 81: '006060', 82: '004040', 34: '006496', 85: '00496d', 86: '00324c', 87: '002638', 49: '4d4d8f', 95: '6f49a4', 96: '54367f', 97: '422a63', 43: 'fa7fff', 99: 'af57af', 100: '824382', 101: '5e315e', 106: '76bdff', 88: '5080ad', 89: '335375', 90: '233c56', 12: 'ffffff', 91: 'e0e0e0', 17: 'afafaf', 102: '808080', 18: '5a5a5a', 94: '404040', 15: '000000'}

min_color = 0
max_color = 106

def get_color_hex(index: int) -> str:
    return colors[index]

def get_color_rgb(index: int) -> Tuple[int, int, int]:
    col_hex = get_color_hex(index)
    return int(col_hex[0:2], 16), int(col_hex[2:4], 16), int(col_hex[4:6], 16)
