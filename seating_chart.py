from PIL import Image, ImageDraw, ImageFont

FONT_FILE = '/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans.ttf'

with open('station coordinates.txt') as coords_file:
    coord_pairs = [[int(part) for part in line.strip().split()] for line in coords_file.readlines()]

with open('students.txt') as students_file:
    students = [student.strip() for student in students_file.readlines()]

print(coord_pairs, students)

font=ImageFont.truetype(FONT_FILE, 36, index=0)

with Image.open('panorama.jpg') as img:
    draw = ImageDraw.Draw(img)

    for coord_pair, student in zip(coord_pairs, students):
        draw.text(coord_pair, student, fill=(255, 0, 255), font=font)

    # Save the edited image
    img.save("seating chart.jpg")
