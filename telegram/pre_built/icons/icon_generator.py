# import json
#
# from PIL import Image
#
# from icons.icon import IconType, Icon, Quality
#
#
# # GENERATOR FOR HD-QUALITY ICON PICTURES
# def generate_icons():
#     info: dict = {}
#     col_1 = (177,177,177)
#     col_2 = (255,255,255)
#     padding_px = 5
#     for type in IconType:
#         icons_of_type = []
#         for num in range(type.value[1], type.value[2]+1):
#             icon = Icon(type, num, Quality.HD, col_1, col_2, False)
#             filename = f"gd_{type.value[0]}_{num}.png"
#             pic = icon.build_icon()
#             box = pic.getbbox()
#             pic = pic.crop(box)
#             pic = Image.alpha_composite(Image.new("RGBA", pic.size, (83,83,83)), pic)
#
#             sz = max(pic.width, pic.height) + 2*padding_px
#             base = Image.new("RGBA", (sz, sz), (83,83,83))
#
#             base.paste(pic, ((sz - pic.width) // 2, (sz - pic.height) // 2))
#
#             base.convert("RGB").save(filename)
#             icons_of_type.append({
#                 "number": icon.icon_number,
#                 "file": filename,
#             })
#             print(f"Generated: {type} {num}")
#
#         info.update({type.value[0]: icons_of_type})
#
#     with open("icons.json", "w+") as f:
#         j = json.dumps(info, indent=2)
#         f.write(j)
#
# if __name__ == '__main__':
#     generate_icons()
