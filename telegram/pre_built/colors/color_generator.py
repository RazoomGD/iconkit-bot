# import json
#
# from PIL import Image
#
# from icons.color import get_color_rgb, get_color_hex, colors
#
#
# # GENERATOR FOR COLORED 40x40 PICTURES
# def generate_colors():
#     info: list = []
#     for id, color in colors.items():
#         color_rgb = get_color_rgb(id)
#         color_hex = get_color_hex(id)
#         filename = f"gd_color_{id}.png"
#         Image.new("RGB", (40, 40), color_rgb).save(filename)
#         info.append({
#             "id": id,
#             "hex": color_hex,
#             "file": filename
#         })
#     with open("colors.json", "w+") as f:
#         j = json.dumps(info, indent=2)
#         f.write(j)
#
# if __name__ == '__main__':
#     generate_colors()
