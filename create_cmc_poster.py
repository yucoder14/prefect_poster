import argparse
import os

from grid_pil import *

def dimension_type(string) -> tuple[int]:
    """Custom type to parse 'WIDTHxHEIGHT' strings."""
    try:
        parts = string.lower().split('x')
        if len(parts) != 2:
            raise ValueError
        return tuple(map(int, parts))
    except ValueError:
        raise argparse.ArgumentTypeError(f"Format must be WIDTHxHEIGHT (e.g., 1024x768). Got: '{string}'")

def grid_type(string) -> tuple[int]:
    """Custom type to parse 'COLxROW' strings."""
    try:
        parts = string.lower().split('x')
        if len(parts) != 2:
            raise ValueError
        # Note: Your prompt specified (-g) {num_col}x{num_row}
        return tuple(map(int, parts))
    except ValueError:
        raise argparse.ArgumentTypeError(f"Format must be COLxROW (e.g., 4x2). Got: '{string}'")

def color_type(string) -> tuple[int]:
    """Parses 'R,G,B' strings into integer tuples."""
    try:
        return tuple(map(int, string.split(',')))
    except ValueError:
        raise argparse.ArgumentTypeError("Color must be R,G,B (e.g., 255,255,255)")

def ratio_type(string) -> float:
    try: 
        parts = string.split('/')
        if len(parts) != 2:
            raise ValueError
        return int(parts[0]) / int(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError(f"Ratio must be WIDTH/HEIGHT (e.g. 4/5). Got: '{string}'")

def main():
    parser = argparse.ArgumentParser(description="create student poster with headshots")

    parser.add_argument('-d', '--dimension', type=dimension_type, default=(1024, 768),
                        help="Page dimensions as WIDTHxHEIGHT (default: 1024x768)")
    parser.add_argument('-g', '--grid', type=grid_type, default=(4, 2),
                        help="Grid size as COLxROW (default: 4x2)")
    parser.add_argument('--background_color', type=color_type, default=(0, 0, 0),
                        help="Background color as R,G,B")
    parser.add_argument('--line_color', type=color_type, default=(255, 255, 255),
                        help="Line color as R,G,B")
    parser.add_argument('--aspect_ratio', type=ratio_type, default=4/5)

    parser.add_argument('--page_margin', type=int, default=40)
    parser.add_argument('--font_path', type=str, required=True)
    parser.add_argument('-i','--image_dir', type=str, required=True)
    parser.add_argument('-o','--out_dir', type=str, default="out")

    args = parser.parse_args()

    # Unpacking for clarity
    page_width, page_height = args.dimension
    num_col, num_row = args.grid

    page_margin = args.page_margin
    aspect_ratio = args.aspect_ratio

    background_color = args.background_color
    line_color = args.line_color

    image_dir = args.image_dir
    font_path = args.font_path
    out_dir = args.out_dir

    assert os.path.exists(image_dir), f"{image_dir} does not exist"
    assert os.path.exists(font_path), f"{font_path} does not exist"

    image_paths = sorted(os.listdir(image_dir), key=lambda path: path.split("_")[-1].lower())
    names = list(map(lambda path: path.split(".")[0].replace("_", " "), image_paths))
    image_paths = list(map(lambda path: Path(image_dir) / path, image_paths))
    images = load_images(image_paths)

    doc = Document(page_width, page_height, page_margin, num_row, num_col, font_path, background_color, line_color)
    doc.draw_headshots(names, images, aspect_ratio, font_size=18, padding=10)
    doc.save(out_dir)

if __name__ == "__main__":
    main()
