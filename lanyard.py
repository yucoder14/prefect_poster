from PIL import Image
import os
import math
import argparse

from grid import PDFGrid

class LanyardDocument(PDFGrid):
    def __init__(self, names, logo):
        super().__init__(num_col=3, cell_aspect_ratio=4/5, page_margin=50, cell_margin=10)

        with open(names, "r") as f:
            self.names = f.readlines()

        self.logo = None
        if logo is not None:
            self.logo = Image.open(logo)
            self.logo_width = 40 

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

            if self.logo is not None: 
                self.draw_image(self.logo, x2 - self.logo_width, y1, self.logo_width)

            j = j + 1

        self.pdf.output("poster.pdf")

if __name__ == "__main__": 
    parser = argparse.ArgumentParser() 
    parser.add_argument("-i", "--input_names_file", required=True)
    parser.add_argument("-l", "--logo",)
    args = parser.parse_args()
    input_names = args.input_names_file
    logo = args.logo
    document = LanyardDocument(input_names, logo)
    document.create_poster()
