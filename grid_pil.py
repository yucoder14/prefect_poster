from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import math
import argparse

def load_images(image_paths): 
    images = list(map(Image.open, image_paths))
     
    return images

def crop_image(image: Image, aspect_ratio: float) -> Image: 
    old_width, old_height = image.size 

    # if width is wider 
    if old_width / old_height > aspect_ratio: 
        new_width = int(old_height * aspect_ratio)
        left = (old_width - new_width) / 2
        top = 0 
        right = (old_width + new_width) / 2
        bottom = old_height
    # if height is taller 
    else:
        new_height = int(old_width / aspect_ratio)
        left = 0
        top = (old_height - new_height) / 2
        right = old_width
        bottom = (old_height + new_height) / 2

    crop_box = (int(left), int(top), int(right), int(bottom))
    cropped_img = image.crop(crop_box)
    return cropped_img

class Cell: 
    def __init__(self, x1:int, x2:int, y1:int, y2:int) -> None:
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    def get_dim(self) -> tuple[int]: 
        return (self.x1, self.x2, self.y1, self.y2)

class Grid: 
    def __init__(self, num_row: int, num_col: int) -> None: 
        self.num_row = num_row
        self.num_col = num_col
        self.cells = []

    def __iter__(self):
        self.i = 0
        return self 

    def __next__(self) -> Cell:
        if self.i < len(self.cells):
            next_cell = self.cells[self.i]
            self.i += 1
            return next_cell
        else:
            raise StopIteration

    def __getitem__(self, key: int) -> Cell:
        return self.cells[key]
    
    def __len__(self) -> int:
        return len(self.cells)

    def init_grid(
        self, 
        page_width: int, 
        page_height: int, 
        page_margin: int, 
        cell_margin: int=5
    ) -> None: 
        assert len(self.cells) == 0, "grid is already initialized"

        canvas_width = page_width - 2 * page_margin
        canvas_height = page_height - 2 * page_margin

        cell_height = canvas_height // self.num_row
        cell_width = canvas_width // self.num_col

        for i in range(self.num_row):
            for j in range(self.num_col):
                x1 = page_margin + j * cell_width
                x2 = page_margin + (j + 1) * cell_width
                y1 = page_margin + i * cell_height
                y2 = page_margin + (i + 1) * cell_height
                self.cells.append(Cell(x1, x2, y1, y2))

class Page:  
    def __init__(
        self, 
        width: int, 
        height: int, 
        page_margin: int, 
        num_row: int,
        num_col: int,
        background_color: tuple[int]=(0,0,0)
    ) -> None: 
        self.page_width = width
        self.page_height = height
        self.page_margin = page_margin
        self.num_row = num_row
        self.num_col = num_col
        self.background_color = background_color

        self.page = Image.new('RGB', (self.page_width, self.page_height), background_color)
        self.grid = Grid(self.num_row, self.num_col)
        self.grid.init_grid(self.page_width, self.page_height, self.page_margin)

    def draw_grid(self, line_color: tuple[int], line_width: int) -> None:  
        draw = ImageDraw.Draw(self.page)

        for cell in self.grid: 
            x1, x2, y1, y2 = cell.get_dim()
            draw.rectangle([(x1, y1), (x2, y2)], outline=line_color, width=line_width)

    def fill_grid_images(self, images: list[Image], aspect_ratio: float, padding:int = 5) -> None:
        assert len(images) <= len(self.grid), "more images than available grids"
        draw = ImageDraw.Draw(self.page)

        for i in range(len(images)):
            cell = self.grid[i]
            image = crop_image(images[i], aspect_ratio)

            x1, x2, y1, y2 = cell.get_dim()
            cell_width = x2 - x1
            new_image_width = cell_width - 2 * padding
            new_image_height = int(new_image_width / aspect_ratio)

            rescaled_image = image.resize((new_image_width, new_image_height)) 

            self.page.paste(rescaled_image,(x1 + padding, y1 + padding))
    
    def fill_grid_texts(
            self, 
            texts: list[str], 
            aspect_ratio: int, 
            font_path: str,
            text_color: tuple[int]=(255,255,255),
            font_size: int=24, 
            padding: int=5
        ) -> None:
        assert len(texts) <= len(self.grid), "more texts than available grids"
        draw = ImageDraw.Draw(self.page)
        font = ImageFont.truetype(font_path, font_size)

        for i in range(len(texts)):
            cell = self.grid[i]
            text = texts[i]
            x1, x2, y1, y2 = cell.get_dim()
            cell_width = x2 - x1
            image_height = int((cell_width - 2 * padding) / aspect_ratio)

            x = x1 + cell_width // 2
            y = y1 + image_height + font_size + padding
            draw.text((x, y), text, font=font, fill=text_color, anchor="mm")

    def show(self) -> None:
        self.page.show()

    def save(self, path) -> None:
        self.page.save(path)

class Document: 
    def __init__(
        self, 
        width: int, 
        height: int, 
        page_margin: int, 
        num_row: int,
        num_col: int,
        font_path: str,
        background_color: tuple[int]=(0,0,0),
        line_color: tuple[int]=(255,255,255),
    ):
        self.page_width = width
        self.page_height = height
        self.page_margin = page_margin
        self.num_row = num_row
        self.num_col = num_col
        self.background_color = background_color
        self.line_color = line_color
        self.font_path = font_path
        
        self.pages = []

    def new_page(self) -> None: 
        self.pages.append(Page(self.page_width, self.page_height, self.page_margin, self.num_row, self.num_col, self.background_color))

    def draw_headshots(self, names: list[str], headshots: list[Image], aspect_ratio, font_size=18, padding=10) -> None: 
        assert len(names) == len(headshots), "length of names much match that of headshots"
        num_cells = self.num_row * self.num_col
        num_pages = math.ceil(len(names) / num_cells)

        names_split = [names[i * num_cells: (i + 1) * num_cells] for i in range(num_pages)]
        headshots_split = [headshots[i * num_cells: (i + 1) * num_cells] for i in range(num_pages)]

        for i in range(num_pages):
            self.new_page()
            page = self.pages[i]
            page.fill_grid_images(headshots_split[i], aspect_ratio, padding=padding) 
            page.fill_grid_texts(names_split[i], aspect_ratio, self.font_path, text_color=self.line_color, font_size=font_size, padding=padding) 

    def save(self, out_dir):  
        os.makedirs(out_dir, exist_ok=True)
        for i in range(len(self.pages)):
            self.pages[i].save(f"{out_dir}/page_{i}.bmp")

if __name__ == "__main__":
    page_width = 1024
    page_height = 768
    page_margin = 40

    background_color = (0,0,0) #black
    num_row = 2
    num_col = 4

    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    line_color = (255,255,255) #white

    aspect_ratio = 4/5

    image_dir = "prefects"
    image_paths = sorted(os.listdir(image_dir), key=lambda path: path.split("_")[-1].lower())
    names = list(map(lambda path: path.split(".")[0].replace("_", " "), image_paths))
    image_paths = list(map(lambda path: Path(image_dir) / path, image_paths))
    images = load_images(image_paths)

    doc = Document(page_width, page_height, page_margin, num_row, num_col, font_path, background_color, line_color)
    doc.draw_headshots(names, images, aspect_ratio, font_size=18, padding=10)
    doc.save("test")
