from PIL import Image
import os
import math
from fpdf import FPDF
import argparse

from grid import PDFGrid

class PrefectDocument(PDFGrid):
    def __init__(self, directory_path):
        super().__init__(num_col=4, cell_aspect_ratio=4/5, page_margin=30, cell_margin=10)
        self.pdf.set_font("helvetica", size=11)

        self.images_path = directory_path

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

    def create_poster(self): 
        with os.scandir(self.images_path) as image_iterator:
            images = list(image_iterator)
            cropped_images = [self.crop_image_name(image) for image in images]

        total_rows = math.ceil(len(cropped_images) / self.num_col)
        i = 0
        j = 0 

        for image in sorted(cropped_images, key=lambda tup: tup[0].split()[-1].lower()): 
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
    parser.add_argument("-i", "--input_images_dir", required=True)
    args = parser.parse_args()
    input_images = args.input_images_dir
    document = PrefectDocument(input_images)
    document.create_poster()
