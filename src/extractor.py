import re
from glob import glob
import os
from PIL import Image
import pytesseract

NUM_ROWS = 5
NUM_COLS = 8
TOP_LEFT = 94, 429
PIC_DIMS = 151, 200
SLOP = 5  # to avoid the border
PIC_SPACING = 183, 310
NAME_AREA_HEIGHT = PIC_SPACING[1] - PIC_DIMS[1] - 10
NAME_Y_OFFSET_FROM_PIC_Y = PIC_DIMS[1] + 6
OUTPUT_DIR = 'pics/extracted'
SHOW_IMAGES = True


def process_page(fn):
    with Image.open(fn) as page_image:
        for yi in range(NUM_ROWS):
            y = TOP_LEFT[1] + yi * PIC_SPACING[1]
            name_y = y + NAME_Y_OFFSET_FROM_PIC_Y

            for xi in range(NUM_COLS):
                x = TOP_LEFT[0] + xi * PIC_SPACING[0]
                name_image = page_image.crop((
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
                    cropped = page_image.crop((
                        x,
                        y,
                        x + PIC_DIMS[0] - SLOP,
                        y + PIC_DIMS[1] - SLOP
                    ))
                    if SHOW_IMAGES:
                        cropped.show()
                    cropped.save(f'{OUTPUT_DIR}/{name}.jpg')


if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

for fn in glob('pics/SCAN*.JPG'):
    print(fn)
    process_page(fn)
