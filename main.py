from PIL import Image
import pytesseract
from glob import glob
import os

PICS_PER_PAGE = 8
INTER_PIC_V_SPACING = 254.5
PIC_LEFT_X = 1020
PIC_WIDTH = 272
PIC_HEIGHT = 203
FIRST_PIC_Y = 330
NAME_Y_OFFSET_FROM_PIC_Y = 29
NAME_X = 1344
GRADES = 6, 7, 8
PAGES_PER_GRADE = 4
OUTPUT_DIR = 'pics/extracted'

def make_directories():
    def md(dir: str) -> None:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    md(f'{OUTPUT_DIR}')
    for grade in GRADES:
        md(f'{OUTPUT_DIR}/{grade}')

make_directories()

files = glob('pics/SCAN*.JPG')
files.sort()
for page_index, fn in enumerate(files):
    grade_dir = GRADES[(page_index // PAGES_PER_GRADE)]
    print(fn, grade_dir)
    with Image.open(fn) as im:
        for i in range(PICS_PER_PAGE):
            y = FIRST_PIC_Y + i * INTER_PIC_V_SPACING

            name_y = y + NAME_Y_OFFSET_FROM_PIC_Y
            name_image = im.crop((NAME_X, name_y, NAME_X + 352, name_y + 40))
            if name := pytesseract.image_to_string(name_image).strip():
                cropped = im.crop((PIC_LEFT_X, y, PIC_LEFT_X + PIC_WIDTH, y + PIC_HEIGHT))
                rotated = cropped.transpose(Image.ROTATE_270)
                # rotated.show()
                print(name)
                rotated.save(f'{OUTPUT_DIR}/{grade_dir}/{name}.jpg')
