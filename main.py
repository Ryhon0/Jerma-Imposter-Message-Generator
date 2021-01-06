#!/usr/bin/env python3

from PIL import Image, ImageDraw
import random
import sys

# this codebase is FUCKED

master_im = Image.open("imposter.jpg")
y_coord_split = 22
master_x_dict = {
    "w": [[7, 29]],
    "h": [[30, 43], [85, 98]],
    "e": [[43, 56], [98, 111], [192, 205]],
    "n": [[56, 69], [123, 135]],
    " ": [[69, 75], [111, 116], [215, 220], [238, 244]],
    "t": [[75, 83], [183, 192]],
    "i": [[116, 122], [220, 225]],
    "m": [[122, 143]],
    "p": [[143, 157]],
    "o": [[157, 171]],
    "s": [[171, 183], [225, 238], [244, 257], [270, 283]],
    "r": [[205, 213]],
    "u": [[257, 270]],
    "!": [[282, 289]],
    "😳": [[289, 312]],
    "l": [[30, 34], [85, 88], [187, 189]],
    "c": [[157, 168]],
    "v": [[7, 20]]
}

# [should flip over x axis, should flip over y axis], [x1, x2]
bootleg_x_dict = {
    "a": [[True, False], [146, 155]],
    "q": [[True, False], [143, 155]],
    "b": [[False, True], [143, 157]],
    "d": [[True, True], [143, 157]],
    "y": [[True, True], [30, 41]],
    "f": [[False, True], [75, 83]],
    "j": [[True, False], [78, 83]],
    "g": [[True, False], [143, 155]],
    "z": [[True, False], [171, 183]]
}

if len(sys.argv) > 1:
    args = sys.argv
    args.pop(0)
    input_string = ' '.join(args)
else:
    input_string = input("Your message here: ")

input_string = input_string.lower().replace(":flushed:", "😳")

new_barcode = Image.new('RGB', (len(input_string)*32, master_im.height))
total_width = 0

for i in input_string:
    if i in master_x_dict.keys():
        x_coords = master_x_dict[i][random.randint(
            0, len(master_x_dict[i]) - 1)]
        scan_line = master_im.crop(
            (x_coords[0], 0, x_coords[1], master_im.height))
        new_barcode.paste(scan_line, (total_width, 0))
        total_width += scan_line.width
    elif i in bootleg_x_dict.keys():
        x_coords = bootleg_x_dict[i][1]

        letter = master_im.crop((x_coords[0], 0, x_coords[1], y_coord_split))
        face = master_im.crop(
            (x_coords[0], y_coord_split, x_coords[1], master_im.height))

        # flip over x?
        if bootleg_x_dict[i][0][0]:
            letter = letter.transpose(Image.FLIP_LEFT_RIGHT)
            face = face.transpose(Image.FLIP_LEFT_RIGHT)

        # flip over y?
        if bootleg_x_dict[i][0][1]:
            letter = letter.transpose(Image.FLIP_TOP_BOTTOM)
            face = face.transpose(Image.FLIP_TOP_BOTTOM)

        # epic edge case
        if i == "a":
            draw = ImageDraw.Draw(letter)
            draw.rectangle([5, 13, 8, 16], fill=(255, 255, 255, 255))

        scan_line = Image.new(
            'RGB', (letter.width, letter.height + face.height))
        scan_line.paste(letter, (0, 0))
        scan_line.paste(face, (0, y_coord_split))
        new_barcode.paste(scan_line, (total_width, 0))
        total_width += scan_line.width
    else:
        print(i + ": LETTER NOT SUPPORTED")

new_barcode = new_barcode.crop((0, 0, total_width, master_im.height))
new_barcode.save(input_string + ".png", "png")
new_barcode.show()
