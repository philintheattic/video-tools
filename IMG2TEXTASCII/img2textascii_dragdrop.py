# -*- coding: UTF-8 -*-

from PIL import Image, ImageDraw, ImageFont
import sys

input_file = sys.argv[1]
output_file = input_file[:-4] + "_textascii.png"

scaleFactor = 0.09
oneCharWidth = 10
oneCharHeight = 18

im = Image.open(input_file)

fnt = ImageFont.truetype('assets/lucon.ttf', 15)

with open("assets/fulltext.txt") as f:
    fulltext = f.read().replace("\n", " ")

width, height = im.size
im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
width, height = im.size
pix = im.load()

outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (0, 0, 0))
d = ImageDraw.Draw(outputImage)
count = 0

#print(len(fulltext))

for i in range(height):
    for j in range(width):
        r, g, b = pix[j, i]
        brightn = int((r+g+b)/3)
        d.text((j*oneCharWidth, i*oneCharHeight), fulltext[count], font=fnt, fill=(brightn, brightn, brightn))
        if (count < (len(fulltext)-1)):
            count += 1
        else:
            count = 0


outputImage.save(output_file)


