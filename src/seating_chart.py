'Creates seating chart images containing student photos and names'

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from station import Station

FONT_FILE = os.environ['FONT_FILE']  # a font usable with ImageDraw
PICTURES_DIR = os.environ['PICTURES_DIR']  # directory with pictures, with subdirectories for grades
INPUTS_DIR = 'seating-chart-inputs'
OUTPUTS_DIR = 'seating-chart-outputs'
GRADES = 6, 7, 8
TEXT_MARGIN = 6

def file_lines(filename) -> list[str]:
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]

def station_empty(student: str) -> bool: return not student

stations = [Station.from_string(line) for line in file_lines(f'{INPUTS_DIR}/station coordinates.txt')]
font = ImageFont.truetype(FONT_FILE, 24)
text_color = (255, 255, 255)

def draw_text(index: int, student: str, image_pos: np.ndarray, image_width: int):
    draw.text(tuple(image_pos + TEXT_MARGIN), '\n'.join(student.split()), fill=text_color, font=font)

    station_number_str = str(index + 1)
    station_number_width: int = draw.textsize(station_number_str, font=font)[0]
    offset_from_right: int = station_number_width + TEXT_MARGIN
    station_number_loc: np.ndarray = image_pos + (image_width - offset_from_right, TEXT_MARGIN)

    draw.text(station_number_loc, station_number_str, fill=text_color, font=font)

if not os.path.isdir(OUTPUTS_DIR):
    os.mkdir(OUTPUTS_DIR)

for grade in GRADES:
    grade_pictures_dir = f'{PICTURES_DIR}/{grade}'
    students = file_lines(f'{INPUTS_DIR}/students{grade}.txt')

    with Image.open('room.jpg') as img:
        draw = ImageDraw.Draw(img)

        for index, (station, student) in enumerate(zip(stations, students)):
            if station_empty(student): continue
            student_image_filename = f'{grade_pictures_dir}/{student}.jpg'
            if not os.path.exists(student_image_filename):
                print(f'Missing picture for {student}')
                student_image_filename = f'{PICTURES_DIR}/missing.jpg'

            with Image.open(student_image_filename) as stu_img:
                image_top_left: np.ndarray = station.loc - (stu_img.width // 2, stu_img.height // 2)
                img.paste(stu_img, tuple(image_top_left))  # Add the student picture
                draw_text(index, student, image_top_left, stu_img.width)  # Add the name and station #

        img.save(f'{OUTPUTS_DIR}/seating chart {grade}.jpg')
