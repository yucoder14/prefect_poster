from PIL import Image
import os
import math
from fpdf import FPDF
import argparse

class LanyardDocument:
    def __init__(self, names, logo):
        self.pdf = FPDF('P', 'pt', 'Letter')
        self.pdf.set_draw_color(r=0, g=0, b=0) 
        self.pdf.set_line_width(0.8)

        with open(names, "r") as f:
            self.names = f.readlines()

        if logo is not None:
            self.logo = Image.open(logo)
            self.logo_width = 40 

        self.num_col = 3
        self.aspect_ratio = 4 / 5
        self.page_margin = 50
        self.col_width = (self.pdf.w - 2 * self.page_margin) / self.num_col

        min_row_height = self.col_width / self.aspect_ratio
        self.num_row = int(self.pdf.h / min_row_height)
        self.row_height = (self.pdf.h - 2 * self.page_margin) / self.num_row

        self.cell_margin = 10

    def draw_line(self, x1, y1, x2, y2):
        self.pdf.line(x1 = x1, y1 = y1 , x2 = x2 , y2 = y2)

    def draw_box(self, x1, y1, x2, y2):
        self.draw_line(x1, y1, x2, y1)
        self.draw_line(x1, y2, x2, y2)
        self.draw_line(x1, y1, x1, y2)
        self.draw_line(x2, y1, x2, y2)

    def draw_image(self, image, x, y, width):
        self.pdf.image(image, x = x, y = y, w = width)

    def draw_text(self, text_x1, text_x2, text_y2, text):
        text_width = self.pdf.get_string_width(text)
        offset = (text_x2 - text_x1) / 2 - (text_width / 2)
        self.pdf.text(text_x1 + offset, text_y2, text)

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

    def create_poster(self): 
        total_rows = math.ceil(len(self.names) / self.num_col)
        i = 0
        j = 0 

        for name in self.names: 
            if j == self.num_col: 
                j = 0
                i = i + 1
            if (i * self.num_col + j) % (self.num_col * self.num_row) == 0: 
                self.new_page(total_rows - i)

            x1 = self.page_margin + j * self.col_width + self.cell_margin
            x2 = self.page_margin + (j + 1) * self.col_width - self.cell_margin
            y1 = self.page_margin + (i % self.num_row) * self.row_height + self.cell_margin
            y2 = self.page_margin + (i % self.num_row + 1) * self.row_height - self.cell_margin
 
            halfway = y2 - (y2 - y1)/2
            self.pdf.set_font("Times", 'B', size=13)
            self.draw_text(x1, x2, halfway - 30, name)
            self.pdf.set_font("Courier",'I', size=10)
            self.draw_text(x1, x2, halfway + 20, "CS Course Staff")
            self.draw_text(x1, x2, halfway + 70, "Department of Computer")
            self.draw_text(x1, x2, halfway + 80, "Science")

            self.draw_image(self.logo, x2 - self.logo_width, y1, self.logo_width)

            j = j + 1

        self.pdf.output("poster.pdf")

if __name__ == "__main__": 
    parser = argparse.ArgumentParser() 
    parser.add_argument("-i", "--input_names", required=True)
    parser.add_argument("-l", "--logo",)
    args = parser.parse_args()
    input_names = args.input_names
    logo = args.logo
    document = LanyardDocument(input_names, logo)
    document.create_poster()
