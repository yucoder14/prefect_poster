from PIL import Image
import os
import math
from fpdf import FPDF
import argparse


num_col = 4
TARGET_ASPECT_RATIO = 4 / 5

class PrefectDocument:
    def __init__(self, directory_path):
        self.pdf = FPDF('P', 'pt', 'Letter')
        self.pdf.set_font("helvetica", size=11)
        self.pdf.set_draw_color(r=0, g=0, b=0) 
        self.pdf.set_line_width(0.8)

        self.images_path = directory_path

        self.num_col = 4
        self.aspect_ratio = 4 / 5
        self.page_margin = 30
        self.col_width = (self.pdf.w - 2 * self.page_margin) / self.num_col

        min_row_height = self.col_width / self.aspect_ratio
        self.num_row = int(self.pdf.h / min_row_height)
        self.row_height = (self.pdf.h - 2 * self.page_margin) / self.num_row

        self.cell_margin = 10
        self.text_margin = 5

    def draw_line(self, x1, y1, x2, y2):
        self.pdf.line(x1 = x1, y1 = y1 , x2 = x2 , y2 = y2)

    def draw_box(self, x1, y1, x2, y2):
        self.draw_line(x1, y1, x2, y1)
        self.draw_line(x1, y2, x2, y2)
        self.draw_line(x1, y1, x1, y2)
        self.draw_line(x2, y1, x2, y2)

    def draw_image(self, image, x, y, width):
        self.pdf.image(image, x = x, y = y, w = width)

    def draw_text(self, text_x1, text_x2, text_y2, name):
        name_width = self.pdf.get_string_width(name)
        offset = (text_x2 - text_x1) / 2 - (name_width / 2)
        self.pdf.text(text_x1 + offset, text_y2, name)

    def new_page(self, num_row):
        num_row = num_row if (num_row <= self.num_row) else self.num_row
        self.pdf.add_page()

        for i in range(0, self.num_col + 1):
            self.draw_line(self.page_margin + i * self.col_width, 
                           self.page_margin, 
                           self.page_margin + i * self.col_width, 
                           self.page_margin + num_row * self.row_height)

        for i in range(0, num_row + 1):
            self.draw_line(self.page_margin, 
                           self.page_margin + i * self.row_height, 
                           self.pdf.w - self.page_margin, 
                           self.page_margin + i * self.row_height)

    def crop_image_name(self, image): 
        img = Image.open(image)
        old_width, old_height = img.size 

        # if width is wider 
        if old_width / old_height > self.aspect_ratio: 
            new_width = int(old_height * self.aspect_ratio)
            left = (old_width - new_width) / 2
            top = 0 
            right = (old_width + new_width) / 2
            bottom = old_height
        # if height is taller 
        else:
            new_height = int(old_width / self.aspect_ratio)
            left = 0
            top = (old_height - new_height) / 2
            right = old_width
            bottom = (old_height + new_height) / 2

        crop_box = (int(left), int(top), int(right), int(bottom))
        cropped_img = img.crop(crop_box)

        return (image.name.split(".")[0].replace("_", " "), cropped_img)

    def create(self): 
        with os.scandir(self.images_path) as image_iterator:
            images = list(image_iterator)
            cropped_images = [self.crop_image_name(image) for image in images]

        total_rows = math.ceil(len(cropped_images) / self.num_col)
        i = 0
        j = 0 

        for image in cropped_images: 
            if j == self.num_col: 
                j = 0
                i = i + 1
            if (i * self.num_col + j) % (self.num_col * self.num_row) == 0: 
                self.new_page(total_rows - i)

            image_x1 = self.page_margin + j * self.col_width + self.cell_margin
            image_y1 = self.page_margin + (i % self.num_row) * self.row_height + self.cell_margin
            image_x2 = self.page_margin + (j + 1) * self.col_width - self.cell_margin

            image_width = image_x2 - image_x1
            image_height = image_width / self.aspect_ratio
            image_y2 = image_y1 + image_height

            self.draw_image(image[1], image_x1, image_y1, image_width)

            text_x1 = image_x1
            text_x2 = image_x2
            text_y1 = image_y2
            text_y2 = self.page_margin + ((i % self.num_row) + 1) * self.row_height - self.cell_margin
            name = image[0]
            self.draw_text(text_x1, text_x2, text_y2, name)

            j = j + 1

        self.pdf.output("poster.pdf")

if __name__ == "__main__": 
    parser = argparse.ArgumentParser() 
    parser.add_argument("-i", "--input_images", required=True)
    args = parser.parse_args()
    input_images = args.input_images
    document = PrefectDocument(input_images)
    document.create()
