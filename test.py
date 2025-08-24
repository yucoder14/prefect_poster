from PIL import Image
import os
import math
from fpdf import FPDF


num_col = 4
TARGET_ASPECT_RATIO = 4 / 5

def crop_image_to_ratio(target_aspect_ratio, image): 
    img = Image.open(image)
    old_width, old_height = img.size 

    # if width is wider 
    if old_width / old_height > target_aspect_ratio: 
        new_width = int(old_height * target_aspect_ratio)
        left = (old_width - new_width) / 2
        top = 0 
        right = (old_width + new_width) / 2
        bottom = old_height
    # if height is taller 
    else:
        new_height = int(old_width / target_aspect_ratio)
        left = 0
        top = (old_height - new_height) / 2
        right = old_width
        bottom = (old_height + new_height) / 2

    crop_box = (int(left), int(top), int(right), int(bottom))
    cropped_img = img.crop(crop_box)

    return cropped_img

directory_path = "images"
with os.scandir(directory_path) as image_iterator:
    images = list(image_iterator)
    cropped_images = [crop_image_to_ratio(TARGET_ASPECT_RATIO, image) for image in images]

# Create PDF
pdf = FPDF('P', 'pt', 'Letter')
pdf.set_font("helvetica", size=12)
pdf.set_draw_color(r=0, g=0, b=0) 
pdf.set_line_width(0.8)

page_margin = 30
col_width = (pdf.w - 2 * page_margin) / num_col
# minimum height should be able to fit with image with TARGET_ASPECT_RATIO
min_row_height = col_width / TARGET_ASPECT_RATIO
num_row = int(pdf.h / min_row_height)
row_height = (pdf.h - 2 * page_margin) / num_row

def draw_box(pdf, x1, y1, x2, y2):
    pdf.line(x1 = x1, y1 = y1 , x2 = x2 , y2 = y1)
    pdf.line(x1 = x1, y1 = y2 , x2 = x2 , y2 = y2)
    pdf.line(x1 = x1, y1 = y1 , x2 = x1 , y2 = y2)
    pdf.line(x1 = x2, y1 = y1 , x2 = x2 , y2 = y2)

# page setup
pdf.add_page()
draw_box(pdf, page_margin, page_margin, pdf.w - page_margin, pdf.h - page_margin)

for i in range(1, num_col):
    pdf.line(x1= page_margin + i * col_width, 
             y1= page_margin, 
             x2= page_margin + i * col_width, 
             y2= pdf.h - page_margin)

for i in range(1, num_row):
    pdf.line(x1 = page_margin, 
             y1 = page_margin + i * row_height, 
             x2 = pdf.w - page_margin, 
             y2 = page_margin + i * row_height)

cell_margin = 10
text_margin = 5
for i in range(num_row): 
    for j in range(num_col):
        image_x1 = page_margin + j * col_width + cell_margin
        image_y1 = page_margin + i * row_height + cell_margin
        image_x2 = page_margin + (j + 1) * col_width - cell_margin

        image_width = image_x2 - image_x1
        image_height = image_width / TARGET_ASPECT_RATIO
        image_y2 = image_y1 + image_height

        pdf.image(cropped_images[num_row * i + j], x = image_x1, y = image_y1, w = image_width)

        text_x1 = image_x1
        text_x2 = image_x2
        text_y1 = image_y2
        text_y2 = page_margin + (i + 1) * row_height - cell_margin
        name = "First Last" 
        name_width = pdf.get_string_width(name)
        print(name_width)
        offset = (text_x2 - text_x1) / 2 - (name_width / 2)
        pdf.text(text_x1 + offset, text_y2, name)

# Output the PDF
pdf.output("pdf_with_pil_image.pdf")


