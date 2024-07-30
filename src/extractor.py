import re
from glob import glob
import os
from PIL import Image
import pytesseract

NUM_ROWS = 5
NUM_COLS = 7
TOP_LEFT = 150, 538
PIC_DIMS = 184, 225
SLOP = 3  # to avoid the border
PIC_SPACING = 202.5, 312
NAME_AREA_HEIGHT = PIC_SPACING[1] - PIC_DIMS[1] - 10
NAME_Y_OFFSET_FROM_PIC_Y = PIC_DIMS[1] + 8
OUTPUT_DIR = 'pics/extracted'
SHOW_IMAGES = False

if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

files = glob('pics/SCAN*.JPG')
files.sort()
for fn in files:
    print(fn)
    with Image.open(fn) as im:
        for yi in range(NUM_ROWS):
            y = TOP_LEFT[1] + yi * PIC_SPACING[1]
            name_y = y + NAME_Y_OFFSET_FROM_PIC_Y

            for xi in range(NUM_COLS):
                x = TOP_LEFT[0] + xi * PIC_SPACING[0]
                name_image = im.crop((
                    x,
                    name_y,
                    x + PIC_DIMS[0],
                    name_y + NAME_AREA_HEIGHT
                ))
                if SHOW_IMAGES:
                    name_image.show()

                if raw_name := pytesseract.image_to_string(name_image).strip():
                    name = re.sub(r'\n+', ' ', raw_name)
                    print(name)
                    cropped = im.crop((
                        x,
                        y,
                        x + PIC_DIMS[0] - SLOP,
                        y + PIC_DIMS[1]
                    ))
                    if SHOW_IMAGES:
                        cropped.show()
                    cropped.save(f'{OUTPUT_DIR}/{name}.jpg')
