from fpdf import FPDF

class PDFGrid:
    def __init__(self, num_col, cell_aspect_ratio, page_margin, cell_margin):
        self.pdf = FPDF('P', 'pt', 'Letter')
        self.pdf.set_draw_color(r=0, g=0, b=0) 
        self.pdf.set_line_width(0.8)

        self.num_col = num_col
        self.aspect_ratio = cell_aspect_ratio
        self.page_margin = page_margin
        self.col_width = (self.pdf.w - 2 * self.page_margin) / self.num_col

        min_row_height = self.col_width / self.aspect_ratio
        self.num_row = int(self.pdf.h / min_row_height)
        self.row_height = (self.pdf.h - 2 * self.page_margin) / self.num_row

        self.cell_margin = cell_margin

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
        raise NotImplementedError
