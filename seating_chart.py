import os
from PIL import Image, ImageDraw, ImageFont

FONT_FILE = os.environ['FONT_FILE'] # a font usable with ImageDraw
PICTURES_DIR = os.environ['PICTURES_DIR'] # directory with pictures, with subdirectories for grades
GRADES = 6, 7, 8

with open('station coordinates.txt') as coords_file:
    coord_pairs = [[int(part) for part in line.strip().split()] for line in coords_file.readlines()]

for grade in GRADES:
    students_fn = f'students{grade}.txt'
    grade_pictures_dir = f'{PICTURES_DIR}/{grade}'
    with open(students_fn) as students_file:
        students = [student.strip() for student in students_file.readlines()]

    font=ImageFont.truetype(FONT_FILE, 24, index=0)

    with Image.open('panorama.jpg') as img:
        draw = ImageDraw.Draw(img)

        for coord_pair, student in zip(coord_pairs, students):
            if student: # student at this seat?
                stu_img_fn = f'{grade_pictures_dir}/{student}.jpg'
                if os.path.exists(stu_img_fn):
                    with Image.open(stu_img_fn) as stu_img:
                        loc = (coord_pair[0] - stu_img.width // 2, coord_pair[1] - stu_img.height // 2)
                        img.paste(stu_img, loc)
                else:
                    loc = coord_pair
                text_loc = (loc[0] + 3, loc[1] + 3)
                draw.text(text_loc, '\n'.join(student.split()), fill=(255, 255, 255), font=font)

        img.save(f'seating chart {grade}.jpg')
